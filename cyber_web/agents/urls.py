# agents/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.agents, name='agents'),
]