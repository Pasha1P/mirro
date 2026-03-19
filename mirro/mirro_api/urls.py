from django.urls import include, path

from mirro_api import views as views_api

urlpatterns = [
    path('get_xcsrf/',views_api.get_xcsrf,name='get_xcsrf'),
    path('users/',views_api.users,name='users'),
    path('auth/',views_api.auth,name='auth'),
    path('boards/',views_api.boards,name='boards'),
    path('board_id/<int:id_board>/',views_api.board_id,name='board_id'),
    path('boards_id_accesses/<int:id_board>/',views_api.boards_id_accesses,name='boards_id_accesses'),
    path('boards_id_likes/<int:id_board>/',views_api.boards_id_likes,name='boards_id_likes'),
    path('logout',views_api.logout,name='logout'),
]
