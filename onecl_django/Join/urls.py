from django.urls import path
from .views import *

urlpatterns = [
    path('', JoinList.as_view()),
    path('<int:pk>/', JoinDetail.as_view()),
    path('auth_level/', AuthLevelAPI.as_view()),
    path('my_club/', MyClubList.as_view()),
    path('search/', SearchUserAPI.as_view()),
    path('delegate/', DelegateMaster.as_view()),
]