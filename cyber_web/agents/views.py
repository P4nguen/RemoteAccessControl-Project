from django.shortcuts import render
from .models import Agent

def agents(request):
    agents_list = Agent.objects.all()[::-1]
    return render(request, 'agents.html', {'agents': agents_list})