from django.urls import path
from django.shortcuts import render

# Şimdilik views.py boş olduğu için direkt burada basitçe tanımlıyoruz
urlpatterns = [
    path('login/', lambda r: render(r, 'auth/login.html'), name='login'),
    path('register/', lambda r: render(r, 'auth/register.html'), name='register'),
]