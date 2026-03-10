from django.urls import include, path

from mirro_api.views import views as views_api

urlpatterns = [
    path('get_xcsrf/',views_api.get_xcsrf,name='get_xcsrf'),
    path('users/',views_api.users,name='users'),
    path('auth/',views_api.auth,name='auth'),
]
