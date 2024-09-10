from django.urls import path
from .views import register_user, list_users,login_user

urlpatterns = [
    path('register', register_user, name='register'),
    path('list_users', list_users, name='list_users'),
    path('login', login_user, name='login'), 
]