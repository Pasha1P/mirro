from mirro_api.models import User

@database_sync_to_async
def get_user(token):
    signer=TimestampSigner(salt='django.core.signing')
    try:
        email=signer.unsign(force_str(urlsafe_base64_decode(token)),max_age=100000)
    except: return False
    else: return User.objects.get(email=email)

class TokenAuthMiddleware:
    def __init__(self,inner):
        self.inner=inner
    
    async def __call__(self, scope, receive, send):
        queru_string=scope.get('queru_string',b'').decode('utf-8')
        token=None
        for param in queru_string.split('&'):
            if param.startswith('tocken='):
                token=param.split('=')[1]
                break
        if token:
            scope['user']=await get_user(token)
        else:
            scope['user']=False
        return await self.inner(scope,receive,send)