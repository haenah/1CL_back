from django.db import models
from User.models import CustomUser
from Club.models import Club


# Create your models here.
class Message(models.Model):
    club = models.ForeignKey(Club, related_name='message_sent', on_delete=models.CASCADE, blank=True)
    receiver = models.ForeignKey(CustomUser, related_name='message_received', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
