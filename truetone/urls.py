from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from services import views

def home(request):
    return render(request, "base.html")

urlpatterns = [
    path("admin/", admin.site.urls), 
    path('accounts/register/', include('accounts.urls')), 
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('feedback/', include('feedback.urls', namespace='feedback')),  
    path('services/', include('services.urls')),  
    path("", views.service_list, name="home"),
]