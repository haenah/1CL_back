"""onecl_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('User.urls')),
    path('club/', include('Club.urls')),
    path('upload/', include('Image.urls')),
    path('join/', include('Join.urls')),
    path('document/', include('Document.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('message/', include('Message.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)