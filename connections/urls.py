from django.urls import path
from .views import send_friend_request, accept_friend_request, reject_friend_request, list_friends, list_pending_requests

urlpatterns = [
    path('send_friend_request', send_friend_request, name='send_friend_request'),
    path('accept_friend_request', accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request', reject_friend_request, name='reject_friend_request'),
    path('list_friends', list_friends, name='list_friends'),
    path('list_pending_requests', list_pending_requests, name='list_pending_requests'),
]