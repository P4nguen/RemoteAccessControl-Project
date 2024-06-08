from django.shortcuts import render

def dashboard(request):
    return render(request, 'base.html')

def agents(request):
    return render(request, 'agents.html')

def reports(request):
    return render(request, 'reports.html')

def attack(request):
    return render(request, 'attack.html')
