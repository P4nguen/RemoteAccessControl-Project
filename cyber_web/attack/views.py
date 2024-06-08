from django.shortcuts import render
from agents.models import Agent
from .models import Attack

# Create your views here.
def attack(request):
    agents_list = Agent.objects.all()
    attack = Attack.objects.all()[0]
    return render(request, 'attack.html', {'agents': agents_list, 'attack': attack})