from django.urls import path

from . import views

urlpatterns = [
    path('', views.search_within_radius, name='search_within_radius'), 
]
