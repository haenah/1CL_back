from django.urls import path
from .views import (JoinList, JoinDetail)

urlpatterns = [
    path('', JoinList.as_view()),
    path('<int:pk>/', JoinDetail.as_view())
]