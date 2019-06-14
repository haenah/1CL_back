from django.db import models
from User.models import CustomUser
from Club.models import Club

class ImageModel(models.Model):
    name = models.TextField(default='')
    image = models.ImageField(null=True)
    club = models.ForeignKey(Club, related_name='image_club', on_delete=models.CASCADE, null=True)

class FileModel(models.Model):
    name = models.TextField(default='')
    file = models.FileField(null=True)
    user = models.ForeignKey(CustomUser, related_name='fileUploader', on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(Club, related_name='file_club', on_delete=models.CASCADE, null=True)
