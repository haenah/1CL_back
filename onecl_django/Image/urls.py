from django.urls import path
from .views import uploadImageAPI

urlpatterns = [
    path('', uploadImageAPI.as_view()),
]
