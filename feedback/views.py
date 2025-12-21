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

@login_required
def service_owner_dashboard(request):
    # Eğer Admin ise tüm geri bildirimleri görsün
    if request.user.is_superuser:
        feedbacks = Feedback.objects.all().order_by('-date')
    # Eğer Hizmet Sorumlusu ise sadece kendi hizmetininkileri görsün
    elif request.user.managed_services.exists():
        feedbacks = Feedback.objects.filter(service__owner=request.user).order_by('-date')
    # Hiçbiri değilse (Normal User) erişimi engelle
    else:
        return redirect('home')
    
    return render(request, 'feedback/dashboard.html', {
        'feedbacks': feedbacks
    })

@login_required
def user_feedback_list(request):
    # Kullanıcının kendi feedback'lerini çekiyoruz
    user_feedbacks = Feedback.objects.filter(user=request.user).order_by('-date')
    
    # Sayıları hesaplıyoruz
    total_sent = user_feedbacks.count()
    # Şimdilik 'processed' kısmını 0 bırakabiliriz veya 
    # AI analizi bittiğinde 'sentiment' alanı dolu olanları sayabiliriz.
    processed_count = user_feedbacks.exclude(tone__isnull=True).count() 

    return render(request, 'feedback/user_feedback_list.html', {
        'feedbacks': user_feedbacks,
        'total_sent': total_sent,
        'processed_count': processed_count,
    })