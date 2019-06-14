from django.urls import path
from .views import uploadImageAPI, uploadFileAPI

urlpatterns = [
    path('image/', uploadImageAPI.as_view()),
    path('file/', uploadFileAPI.as_view()),
]
