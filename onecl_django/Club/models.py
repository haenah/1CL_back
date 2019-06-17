from django.db import models
from User.models import CustomUser


# Create your models here.
class Dept(models.Model):
    name = models.CharField(primary_key=True, max_length=20)


class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=20)


class Club(models.Model):
    name = models.CharField(max_length=20)
    master = models.ForeignKey(CustomUser, related_name='owing_clubs', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name='clubs_category', on_delete=models.SET_NULL, null=True)
    dept = models.ForeignKey(Dept, related_name='clubs_dept', on_delete=models.SET_NULL, null=True)
    apply_message = models.CharField(max_length=2000, default='지원서는 성의있게 작성해 주세요!')
    intro = models.TextField(default='동아리 소개글을 작성해 주세요.')

    class Meta:
        ordering = ['name']
