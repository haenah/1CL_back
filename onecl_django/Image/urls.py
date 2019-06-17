from django.urls import path
from .views import uploadImageAPI, uploadFileAPI, FileDetail

urlpatterns = [
    path('image/', uploadImageAPI.as_view()),
    path('file/', uploadFileAPI.as_view()),
    path('file/<int:pk>/', FileDetail.as_view()),
]
