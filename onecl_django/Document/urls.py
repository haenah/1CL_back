from django.urls import path
from .views import *

urlpatterns = [
    path('', DocumentList.as_view()),
    path('<int:pk>/', DocumentDetail.as_view()),

]
