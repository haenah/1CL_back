from django.db import models
from User.models import CustomUser
from Club.models import Club
from Join.models import Join

# Create your models here.


class DocumentType(models.Model):
    name = models.CharField(max_length=20)
    club = models.ForeignKey(Club, related_name='types', on_delete=models.CASCADE, null=True, blank=True)


class Document(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=3000)
    date = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(DocumentType, related_name='documents_type', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(CustomUser, related_name='documents_owner', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, related_name='documents_club', on_delete=models.CASCADE, null=True)
    view = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date', 'title', 'content', 'owner__name']


class Comment(models.Model):
    content = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, related_name='comment', on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(Document, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
