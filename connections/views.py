from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import *

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    user = request.user
    friend_id = request.data.get('friend_id')

    try:
        friend = User.objects.get(id=friend_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    existing_friendship = Friendship.objects.filter(user=user, friend=friend).first()
    if existing_friendship:
        return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    recent_requests_count = Friendship.objects.filter(user=user, created_at__gte=one_minute_ago).count()
    if recent_requests_count >= 3:
        return Response({'detail': 'You cannot send more than 3 friend requests within a minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    friendship = Friendship.objects.create(user=user, friend=friend)
    return Response({'detail': 'Friend request sent.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    user = request.user
    friend_id = request.data.get('friend_id')

    try:
        friend = User.objects.get(id=friend_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    friendship = Friendship.objects.filter(user=friend, friend=user, accepted=False).first()
    if not friendship:
        return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
    friendship.accepted = True
    friendship.save()
    return Response({'detail': 'Friend request accepted.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
    user = request.user
    friend_id = request.data.get('friend_id')
    try:
        friend = User.objects.get(id=friend_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    friendship = Friendship.objects.filter(user=friend, friend=user, accepted=False).first()
    if not friendship:
        return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
    friendship.delete()
    return Response({'detail': 'Friend request rejected.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    user = request.user
    friendships = Friendship.objects.filter(user=user, accepted=True)
    friends = [friendship.friend for friendship in friendships]
    friend_data = [{'id': friend.id, 'email': friend.email} for friend in friends]
    return Response({'friends': friend_data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    user = request.user
    pending_requests = Friendship.objects.filter(friend=user, accepted=False)
    request_data = [{'id': friendship.user.id, 'email': friendship.user.email} for friendship in pending_requests]

    return Response({'pending_requests': request_data}, status=200)