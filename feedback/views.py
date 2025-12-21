from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from services.models import Service 
from .forms import FeedbackForm
from .models import Feedback

@login_required 
def submit_feedback(request, service_id): 
    service = get_object_or_404(Service, id=service_id) 
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user 
            feedback.service = service   
            feedback.save() 
            return render(request, 'feedback/success.html', {'feedback': feedback})
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit_feedback.html', {
        'form': form,
        'service': service
    })

# --- USER DASHBOARD (Aleyna's Stats Included) ---
@login_required
def user_feedback_list(request):
    """Kullanıcının kendi gönderdiği feedback'leri istatistiklerle listeler"""
    user_feedbacks = Feedback.objects.filter(user=request.user).order_by('-date')
    
    # Aleyna'nın eklediği sayaçlar
    total_sent = user_feedbacks.count()
    processed_count = user_feedbacks.exclude(tone__isnull=True).count() 

    return render(request, 'feedback/user_feedback_list.html', {
        'feedbacks': user_feedbacks,
        'total_sent': total_sent,
        'processed_count': processed_count,
    })

# --- SERVICE OWNER DASHBOARD (Cansu's Logic & Aleyna's Design Context) ---
@login_required
def service_owner_dashboard(request):
    """Servis sahibine veya Admin'e gelen feedback'leri listeler"""
    
    # Cansu'nun eklediği Admin ve Sorumlu kontrolü
    if request.user.is_superuser:
        # Admin her şeyi görür
        feedbacks = Feedback.objects.all().order_by('-date')
    elif request.user.managed_services.exists():
        # Sorumlu sadece kendi hizmetlerini görür
        feedbacks = Feedback.objects.filter(service__owner=request.user).order_by('-date')
    else:
        # Yetkisiz kullanıcıyı ana sayfaya atar
        return redirect('home')
    
    return render(request, 'feedback/dashboard.html', {
        'feedbacks': feedbacks
    })