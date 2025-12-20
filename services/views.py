from django.shortcuts import render
from .models import Service 

def service_list(request):
    # Veritabanındaki tüm servisleri çek (FR-7 ve FR-55 gereksinimi)
    services = Service.objects.all() 
    return render(request, 'services/service_list.html', {'services': services})