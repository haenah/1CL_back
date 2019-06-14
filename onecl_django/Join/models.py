from django.db import models
from User.models import CustomUser
from Club.models import Club


# Create your models here.
class Join(models.Model):
    user = models.ForeignKey(CustomUser, related_name='clubs', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, related_name='members', on_delete=models.CASCADE)
    auth_level = models.IntegerField(default=1)

    # 잘 모르겠다
    class Meta:
        ordering = ['-auth_level', 'user__name', ]
        unique_together = ['user', 'club']
