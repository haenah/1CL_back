from django.db import models

class ImageModel(models.Model) :
    name = models.TextField(default='')
    image = models.ImageField(null=True)