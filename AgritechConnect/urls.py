from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('weather/', views.weather, name='weather'),
    path('delete/<int:city_id>/', views.delete_city, name='delete_city'),
]
