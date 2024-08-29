from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('weather/', views.weather, name='weather'),
    path('delete/<int:city_id>/', views.delete_city, name='delete_city'),
    path('contact/', views.contact, name='contact'),
    path('messages/', views.messages_view, name='messages'),
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/<int:post_id>/', views.forum_detail, name='forum_detail'),
    path('forum/create/', views.create_post, name='create_post'),
    path('best_practices/', views.best_practices, name='best_practices'),
    path('market-info/', views.market_info, name='market_info'),
]
