from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from services import models
from services.models import Service 
from .forms import FeedbackForm
from .models import Feedback
from django.db.models import Q
from .utils import analyze_feedback_with_ai

@login_required 
def submit_feedback(request, service_id): 
    service = get_object_or_404(Service, id=service_id) 
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user 
            feedback.service = service 
            # --- AI ANALİZİ BURADA BAŞLIYOR ---
            analysis = analyze_feedback_with_ai(feedback.raw_text)
            if analysis:
                feedback.category = analysis.get('category', 'other')
                feedback.severity = analysis.get('severity', 1)
                feedback.tone = analysis.get('tone', 'neutral')
                feedback.intent = analysis.get('intent', 'complaint')
            # ---------------------------------  
            feedback.save() 
            return render(request, 'feedback/success.html', {'feedback': feedback})
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit_feedback.html', {
        'form': form,
        'service': service
    })

# --- USER DASHBOARD (Updated with Week 2 Filters) ---
@login_required
def user_feedback_list(request):
    """Kullanıcının kendi feedback'lerini filtreleme ve istatistiklerle listeler"""
    
    # 1. Temel Sorgu: Kullanıcının kendi verileri
    query_set = Feedback.objects.filter(user=request.user).order_by('-date')

    # 2. Hafta 1. Gün: Filtreleme Mantığı
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    severity_filter = request.GET.get('severity', '')

    # Arama filtresi
    if search_query:
        query_set = query_set.filter(raw_text__icontains=search_query)

   # Durum (Status) filtresi
    if status_filter == 'processed':
        query_set = query_set.exclude(normalized_text__isnull=True).exclude(normalized_text="")
    elif status_filter == 'pending':
        query_set = query_set.filter(Q(normalized_text__isnull=True) | Q(normalized_text=""))
   
   # Önem Derecesi (Severity) filtresi
    if severity_filter and severity_filter != '':
        # KRİTİK: Modelde IntegerField olduğu için int() çevrimi şart
        query_set = query_set.filter(severity=int(severity_filter))

    # 3. İstatistik Sayaçları (Filtrelemeden bağımsız ana sayılar)
    base_user_data = Feedback.objects.filter(user=request.user)
    total_sent = base_user_data.count()
    processed_count = base_user_data.exclude(normalized_text__isnull=True).exclude(normalized_text="").count()
    return render(request, 'feedback/user_feedback_list.html', {
        'feedbacks': query_set,       # Filtrelenmiş liste
        'total_sent': total_sent,     # İstatistik Kartı 1
        'processed_count': processed_count, # İstatistik Kartı 2
        # Filtre değerlerini geri gönderiyoruz ki sayfada seçili kalsınlar
        'current_status': status_filter,
        'current_severity': severity_filter,
        'q': search_query,
    })

# --- SERVICE OWNER DASHBOARD (Cansu's Logic Preserved) ---
@login_required
def service_owner_dashboard(request):
    """Servis sahibine veya Admin'e gelen feedback'leri listeler"""
    
    # Cansu'nun güvenlik kontrollerini koruyoruz
    if request.user.is_superuser:
        feedbacks = Feedback.objects.all().order_by('-date')
    elif request.user.managed_services.exists():
        feedbacks = Feedback.objects.filter(service__owner=request.user).order_by('-date')
    else:
        return redirect('home')
    
    return render(request, 'feedback/dashboard.html', {
        'feedbacks': feedbacks
    })