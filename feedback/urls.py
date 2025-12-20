from django.urls import path
from . import views
from .views import submit_feedback

app_name = 'feedback'

urlpatterns = [
    path('submit/<int:service_id>/', submit_feedback, name='submit_feedback'),
    path('dashboard/', views.service_owner_dashboard, name='service_owner_dashboard'),
]