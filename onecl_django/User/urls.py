from django.contrib import admin
from django.urls import path, include
from .views import RegistrationAPI, LoginAPI, UserAPI, DuplicateEmailAPI, DuplicateUserIdAPI, CodeVerificationAPI

urlpatterns = [
    path('auth/register/', RegistrationAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
    path('auth/user/', UserAPI.as_view()),
    path('auth/email/', DuplicateEmailAPI.as_view()),
    path('auth/id/', DuplicateUserIdAPI.as_view()),
    path('auth/code/', CodeVerificationAPI.as_view()),
]
