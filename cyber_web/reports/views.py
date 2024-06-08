from django.shortcuts import render
from .models import Report

# Create your views here.
def reports(request):
    report_list = Report.objects.all()[::-1]
    return render(request, 'reports.html', {'reports': report_list})