"""urls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path

from rest_framework import routers
from heyurl import views

router = routers.DefaultRouter()
router.register(r'urls', views.UrlViewSet, basename='urls')

urlpatterns = [
    path('', include('heyurl.routes.web')),
    path('u/<short_url>/', include('heyurl.routes.short_url')),
    path('', include(router.urls)),
]
