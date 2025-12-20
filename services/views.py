from django.shortcuts import render
from .models import Service # Service modelinin burada tanımlı olduğundan emin ol

def service_list(request):
    # Veritabanındaki tüm servisleri çek (FR-7 ve FR-55 gereksinimi)
    services = Service.objects.all() 
    # Aleyna'nın hazırladığı template'e verileri gönder
    return render(request, 'services/service_list.html', {'services': services})