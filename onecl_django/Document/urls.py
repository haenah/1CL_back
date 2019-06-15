from django.urls import path
from .views import *

urlpatterns = [
    path('', DocumentList.as_view()),
    path('<int:pk>/', DocumentDetail.as_view()),
    path('doc_type/', DocumentTypeList.as_view()),
    path('doc_type/<int:pk>', DocumentTypeDetail.as_view()),
    path('comment/', CommentList.as_view()),
    path('comment/<int:pk>/', CommentDetail.as_view()),
]
