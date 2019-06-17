from django.urls import path
from .views import *

urlpatterns = [
    path('', MessageList.as_view()),
    path('<int:pk>/', MessageDetail.as_view()),
    path('delete_all/', DeleteReadMessage.as_view()),
]
