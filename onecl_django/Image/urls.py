from django.urls import path
from .views import uploadImageAPI, uploadFileAPI, FileDetailAPI

urlpatterns = [
    path('image/', uploadImageAPI.as_view()),
    path('file/', uploadFileAPI.as_view()),
    path('file/<int:pk>/', FileDetailAPI.as_view()),
]
