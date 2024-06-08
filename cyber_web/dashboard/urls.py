from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('agents/', views.agents, name='agents'),
    path('reports/', views.reports, name='reports'),
    path('attack/', views.attack, name='attack'),
]
