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
    apply_message = models.CharField(max_length=2000, default='welcome')

    class Meta:
        ordering = ['name']
