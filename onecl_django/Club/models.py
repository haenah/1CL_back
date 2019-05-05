from django.db import models
from User.models import CustomUser


# Create your models here.
class Dept(models.Model):
    name = models.CharField(primary_key=True, max_length=20)


class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=20)


class Club(models.Model):
    name = models.CharField(max_length=20)
    master = models.ForeignKey(CustomUser, related_name='owing_club', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='club', on_delete=models.SET('default'))
    dept = models.ForeignKey(Dept, related_name='club', on_delete=models.SET('default'))
