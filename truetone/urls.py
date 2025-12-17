from django.contrib import admin
from django.urls import path
from django.shortcuts import render

def home(request):
    return render(request, "base.html")

def login_view(request):
    return render(request, "auth/login.html")

def register_view(request):
    return render(request, "auth/register.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
]
