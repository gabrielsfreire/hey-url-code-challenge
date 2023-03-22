from django.urls import path

from heyurl import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store', views.store, name='store'),
    path('metric-panel/<short_url>/', views.metric_panel, name='metric-panel'),
]
