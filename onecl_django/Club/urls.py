from django.urls import path
from .views import (ClubList, ClubDetail, CategoryList, DeptList)

urlpatterns = [
    path('', ClubList.as_view()),
    path('<int:pk>/', ClubDetail.as_view()),
    path('category/', CategoryList.as_view()),
    path('dept/', DeptList.as_view()),
]