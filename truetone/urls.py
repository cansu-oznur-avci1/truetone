from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, "base.html")

urlpatterns = [
    path("admin/", admin.site.urls), 
    path('accounts/', include('accounts.urls')), 
    path('feedback/', include('feedback.urls')),  
    path('services/', include('services.urls')),  
    path("", home, name="home"),
]