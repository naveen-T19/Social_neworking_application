from django.db import models
from django.conf import settings


class Friendship(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friends', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)  # Indicates if the friendship is accepted
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the request was created

    def __str__(self):
        return f"{self.user} - {self.friend} ({'Accepted' if self.accepted else 'Pending'})"