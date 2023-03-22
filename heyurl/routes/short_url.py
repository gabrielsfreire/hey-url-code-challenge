from django.urls import path

from heyurl import views

urlpatterns = [
    path('', views.short_url_click, name='short_url'),
]
