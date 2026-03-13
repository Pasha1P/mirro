from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.signing import TimestampSigner
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, QueryDict
from django.middleware.csrf import get_token
from django.template.context_processors import request
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from mirro_api.models import Like, Shape, User, Board, AccessToEdit


def get_xcsrf(request):
    data = {
        'X-CSRFToken': get_token(request)
    }
    return JsonResponse(data, safe=False, status=200)

def is_auth(request):
    if not request.headers.get('Authorization'):
        return False
    token = request.headers.get('Authorization').split(' ')[-1]
    signer = TimestampSigner(salt='django.core.signing')
    try:
        email = signer.unsign(force_str(urlsafe_base64_decode(token)), max_age=1000)
    except:
        return False
    else:
        user = User.objects.get(email=email)
        return user

def users(request):
    if request.method == 'POST':
        if is_auth(request):
            return JsonResponse({'code': 403, 'message': 'Доступ запрещён'}, safe=False, status=403)
        data = {
            # 'user': {},
        }
        error422 = {
            # 'errors': {},
            'code': 422,
            'message': 'Некорректные данные'
        }
        errors = {
            'username': [],
            'email': [],
            'password': [],
        }

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ОШИБКИ
        if not username or username == ' ':
            errors['username'].append('Поле не должно быть пустым')
        elif not username.isalpha() or not username.isascii():
            errors['username'].append('Поле должно содержать только латиницу')

        if not password or password == ' ':
            errors['password'].append('Поле не должно быть пустым')
        elif len(password) < 8 or not any(not char.isalnum() for char in password) or not any(char.isdigit() for char in password):
            errors['password'].append('Пароль должен быть больше 8 символов, должен содержать спецсимволы и цифры')

        if not email or email == ' ':
            errors['email'].append('Поле не должно быть пустым')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            errors['email'].append('Пользователь с таким email уже существует')

        for key in list(errors.keys()):
            if not errors[key]:
                del errors[key]

        if errors:
            error422['errors'] = errors
            return JsonResponse(error422, safe=False, status=422)

        hasher = PBKDF2PasswordHasher()
        hash_password = hasher.encode(password, salt='extra')
        user = User(username=username, email=email, password=hash_password)
        user.save()

        data['user'] = {
            'username': user.username,
            'email': user.email,
        }
        return JsonResponse({'code': 201, 'message': 'Пользователь добавлен', 'data': data}, safe=False, status=201)



def auth(request):
    if request.method == 'POST':
        if is_auth(request):
            return JsonResponse({'code': 403, 'message': 'Доступ запрещён'}, safe=False, status=403)

    data = {
        # 'user': {},
        # 'token': {},
    }
    error422 = {
        # 'errors':{},
        'code': 422,
        'message': 'Некорректные данные',
    }
    errors = {
        'email': [],
        'password': [],
    }

    email = request.POST.get('email')
    password = request.POST.get('password')

    if not email or ' ' in email:
        errors['email'].append('Поле не должно быть пустым')
    if not password or ' ' in password:
        errors['password'].append('Поле не должно быть пустым')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    if not user:
        errors['email'].append('Пользователь с таким email не существует')

    for key in list(errors.keys()):
        if not errors[key]:
            del errors[key]

    if errors:
        error422['errors'] = errors
        return JsonResponse(error422, safe=False, status=422)

    hasher = PBKDF2PasswordHasher()
    if not hasher.verify(password, user.password):
        return JsonResponse({'code': 401, 'message': 'Пользователь не авторизован'}, safe=False, status=401)

    data['user'] = {
        'id_user': user.pk_user,
        'username': user.username,
        'email': user.email,
    }
    signer = TimestampSigner(salt='django.core.signing')
    token = urlsafe_base64_encode(force_bytes(signer.sign(user.email)))
    data['token'] = token

    return JsonResponse({'code': 200, 'data': data}, safe=False, status=200)


def boards(request):
    user = is_auth(request)
    if request.method == "POST":
        if not user:
            return JsonResponse({'code': 401,'message': 'Пользователь не авторизирован'}, safe=False, status=401)

        title = request.POST.get('title')
        if not title or title.strip() == '':
            return JsonResponse({'code': 422, 'message':'Поле не должен быть пустым'}, safe=False, status=422)

        board = Board.objects.create(
            title = title,
            is_published = 0,
            total_like = 1,
        )
        AccessToEdit.objects.create(
            author = 1,
            fk_user = user,
            fk_board = board
        )
        return JsonResponse({
            'code': 201,
            'message': 'Доска создана',
            'data': {
                'id_board': board.pk_board
            }
        }, safe=False, status=201)

    elif request.method == 'GET':
        if not user:
            return JsonResponse({'code': 401,'message': 'Пользователь не авторизирован'}, safe=False, status=401)

        filter_param = request.GET.get('filter', 'published')
        accessed_ids = AccessToEdit.objects.filter(fk_user = user).values_list('fk_board', flat=True)

        if filter_param == 'all':
            # доски, которые публичные или к которым есть доступ у пользователя, при чем авторство или соавторство
            queryset = Board.objects.filter(Q(is_published = 1) | Q(pk_board__in = accessed_ids))
        elif filter_param == 'accessed': # доски, к которым есть доступ (автор/соавтор)
            queryset = Board.objects.filter(pk_board__in = accessed_ids)
        else: # только публичные
            queryset = Board.objects.filter(is_published = 1)

        if request.GET.get('sort') == 'likes':
            queryset = queryset.order_by('-total_likes')

        boards_list = []

        for board in queryset:
            ower_entry = AccessToEdit.objects.filter(fk_board = board, author = 1).select_related('fk_user').first()
            boards_list.append({
                'id_board': board.pk_board,
                'title': board.title,
                'likes': board.total_like,
                'is_published': bool(board.is_published),
                'username': ower_entry.fk_user.username,
            })

        return JsonResponse({'data':boards_list}, safe=False, status=200)
    
def board_id(request,id_board):
    try: board=Board.objects.get(pk_board=id_board)
    except Board.DoesNotExist: return JsonResponse({'code':'404','message':'ресурс не найден','data':board},safe=False,status=404)
    
    user=is_auth(request)
    if user is None: return JsonResponse({'code': 401,'message': 'Пользователь не авторизирован'}, safe=False, status=401)
    
    is_owner = AccessToEdit.objects.filter(fk_board=board, fk_user=user,author=1)
    if not is_owner.exists():  return JsonResponse({'code': 403,'message': 'недостаточно прав'}, safe=False, status=403)

    if request.method in ['PUT', 'PATCH']:
        put_data = QueryDict(request.body)
        title = put_data.get('title')
        published = int(put_data.get('published'))

        mass={}
        if title:
            if not title.strip(): return JsonResponse({'code':'422','message':'проваленнв валидация данных','data':title},safe=False,status=422)
            mass['title']=title
        if published:
            if published not in [1,0]: return JsonResponse({'code':'422','message':'проваленнв валидация данных','data':published},safe=False,status=422)
            mass['title']=title
        if not mass: return JsonResponse({'code': '400', 'message': 'нет данных для обновления'}, status=400)
        Board.objects.filter(pk_board=id_board).update(**mass)
        return JsonResponse({'code': '201', 'message': 'доска обновленна'}, status=201)
    
    if request.method == 'DELETE':
        Shape.objects.filter(fk_board=board).delete()
        Like.objects.filter(fk_board=board).delete()
        AccessToEdit.objects.filter(fk_board=board).delete()
        board.delete()
        return JsonResponse({'code':200,'message':'доска удаленна'},safe=False,status=200)
        
def boards_id_accesses(request, id_board):
    user=is_auth(request)
    if user is None: return JsonResponse({'code': 401,'message': 'Пользователь не авторизирован'}, safe=False, status=401)
    
    try: board=Board.objects.get(pk_board=id_board)
    except Board.DoesNotExist: return JsonResponse({'code':'404','message':'ресурс не найден'},safe=False,status=404)
    
    is_owner = AccessToEdit.objects.filter(fk_board=board, fk_user=user,author=1)
    if not is_owner.exists():  return JsonResponse({'code': 403,'message': 'недостаточно прав'}, safe=False, status=403)

    if request.method == 'GET':
        acces = AccessToEdit.objects.filter(author=0,fk_board=board)
        JsonResponse({'code':200,'message':'список соавторов','data':list(acces)},safe=False,status=200)
        
    if request.method == 'POST':
        email =request.POST.get('target_email')
        try: email_user = User.objects.get(email=email)
        except User.DoesNotExist: return JsonResponse({'code':'404','message':'ресурс не найден'},safe=False,status=404)
        access,created=AccessToEdit.objects.get_or_create(fk_user=email_user,fk_board=board,defaults={'author':0})
        if created:return JsonResponse({'code':'201','message':'пользователь создан','data':access},safe=False,status=201)
        else: return JsonResponse({'code':'422','message':'проваленна валидация данных'},safe=False,status=422)
    
    if request.method == 'DELETE':
        email=request.get('target_email').strip()
        if not email: return JsonResponse({'code':'422','message':'проваленна валидация данных'},safe=False,status=422)
        try: email_user=User.objects.get(email=email)
        except User.DoesNotExist:return JsonResponse({'code':'404','message':'ресурс не найден'},safe=False,status=404)
        if user in email_user: return JsonResponse({'code':'403','message':'недостаточно прав'},safe=False,status=403)
        deleted, _ = AccessToEdit.objects.filter(fk_user=email_user,fk_board=board,author=0).delete()
        if deleted:return JsonResponse({'code': 200, 'message': 'ресурс удалён'},status=200)
        return JsonResponse({'code': 404, 'message': 'ресурс не найден'},status=404)

def boards_id_likes(request, id_board):
    user=is_auth(request)
    if user is None: return JsonResponse({'code': 401,'message': 'Пользователь не авторизирован'}, safe=False, status=401)
    try: board=Board.objects.get(pk_board=id_board)
    except Board.DoesNotExist: return JsonResponse({'code':'404','message':'ресурс не найден'},safe=False,status=404)

    if request.method == 'GET':
        is_owner = AccessToEdit.objects.filter(fk_board=board, fk_user=user,author=1)
        if not is_owner.exists():  return JsonResponse({'code': 403,'message': 'недостаточно прав'}, safe=False, status=403)
        return JsonResponse({'code':'201','message':'список лайкнувших','data':list(Like.objects.filter(fk_board=board).values())},safe=False,status=201)

    if request.method == 'POST':
        access,_=Like.objects.get_or_create(fk_user=user,fk_board=board)
        if access:return JsonResponse({'code': 201, 'message': 'лайк поставлен'},status=201)
        return JsonResponse({'code': 422, 'message': 'лайк уже стоит'},status=422)

    if request.method == 'DELETE':
        try: like=Like.objects.get(fk_user=user,fk_board=board)
        except Like.DoesNotExist:return JsonResponse({'code':'404','message':'ресурс не найден'},safe=False,status=404)
        like.delete()
        return JsonResponse({'code': 200, 'message': 'ресурс удалён'},status=200)