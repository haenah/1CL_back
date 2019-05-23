from django.urls import path
from .views import RegistrationAPI, LoginAPI, UserAPI, DuplicateEmailAPI, DuplicateUserIdAPI, CodeVerificationAPI

urlpatterns = [
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('user/', UserAPI.as_view()),
    path('email/', DuplicateEmailAPI.as_view()),
    path('id/', DuplicateUserIdAPI.as_view()),
    path('code/', CodeVerificationAPI.as_view())
]
