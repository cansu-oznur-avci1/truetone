from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from services import views

def home(request):
    return render(request, "base.html")

urlpatterns = [
    path("admin/", admin.site.urls), 
    path('accounts/', include('accounts.urls')), 
    path('feedback/', include('feedback.urls', namespace='feedback')),  
    path('services/', include('services.urls')),  
    path("", views.service_list, name="home"),
]