from django.shortcuts import render

from django.shortcuts import render, redirect 
from .forms import RegisterForm 

def register(request):
    if request.method == 'POST':
        print("Gelen POST verisi:", request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Kayıt başarılıysa Login sayfasına gönder
            return redirect('login') 
        else:
           print("HATA DETAYI:", form.errors)
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})