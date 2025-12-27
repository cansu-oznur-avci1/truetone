import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils.dateparse import parse_date
from services.models import Service 
from .forms import FeedbackForm
from .models import Feedback
from .utils import analyze_feedback_with_ai

@login_required 
def submit_feedback(request, service_id): 
    """Kullanıcının geri bildirim gönderdiği ve AI analizinin tetiklendiği yer"""
    service = get_object_or_404(Service, id=service_id) 
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user 
            feedback.service = service 
            
            # --- AI ANALİZİ ---
            analysis = analyze_feedback_with_ai(feedback.raw_text)
            if analysis:
                feedback.category = str(analysis.get('category', 'other')).lower()
                feedback.severity = int(analysis.get('severity', 1))
                feedback.tone = str(analysis.get('tone', 'neutral')).lower()
                feedback.intent = str(analysis.get('intent', 'complaint')).lower()
                feedback.normalized_text = analysis.get('normalized_text', feedback.raw_text)
            
            feedback.save() 
            return render(request, 'feedback/success.html', {'feedback': feedback})
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit_feedback.html', {
        'form': form,
        'service': service
    })

@login_required
def user_feedback_list(request):
    """Kullanıcının kendi feedback geçmişini gördüğü yer"""
    query_set = Feedback.objects.filter(user=request.user).order_by('-date')

    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    severity_filter = request.GET.get('severity', '')

    if search_query:
        query_set = query_set.filter(raw_text__icontains=search_query)

    if status_filter == 'processed':
        query_set = query_set.exclude(normalized_text__isnull=True).exclude(normalized_text="")
    elif status_filter == 'pending':
        query_set = query_set.filter(Q(normalized_text__isnull=True) | Q(normalized_text=""))

    if severity_filter and severity_filter != '':
        query_set = query_set.filter(severity=int(severity_filter))

    # İstatistikler
    base_user_data = Feedback.objects.filter(user=request.user)
    total_sent = base_user_data.count()
    processed_count = base_user_data.exclude(normalized_text__isnull=True).exclude(normalized_text="").count()

    return render(request, 'feedback/user_feedback_list.html', {
        'feedbacks': query_set,
        'total_sent': total_sent,
        'processed_count': processed_count,
        'current_status': status_filter,
        'current_severity': severity_filter,
        'q': search_query,
    })

@login_required
def service_owner_dashboard(request):
    """
    Admin: Tüm servisleri isme/tarihe göre filtreleyebilir.
    Service Owner: Sadece kendi servislerini tarihe göre filtreler.
    Grafik: Filtrelenmiş verilere göre servis dağılımını (Library, IT vb.) gösterir.
    """
    
    # 1. YETKİ KONTROLÜ (Cansu'nun korunan mantığı)
    if request.user.is_superuser:
        # Admin her şeyi görebilir
        feedbacks = Feedback.objects.all().order_by('-date')
    elif request.user.managed_services.exists():
        # Service Owner sadece kendi servislerini görebilir
        feedbacks = Feedback.objects.filter(service__owner=request.user).order_by('-date')
    else:
        return redirect('home')

    # 2. FİLTRELERİ YAKALA (Senin filtreleme mantığın)
    search_query = request.GET.get('q', '')         # İsim/Metin arama
    status_filter = request.GET.get('status', '')   # AI Durumu
    severity_filter = request.GET.get('severity', '') # Önem Derecesi
    start_date = request.GET.get('start_date', '')   # Başlangıç Tarihi
    end_date = request.GET.get('end_date', '')       # Bitiş Tarihi

    # 3. DİNAMİK FİLTRELEME UYGULAMA (Selection Procedure)
    # Admin isme göre filtreleyebilir (Örn: Library aratınca grafik ona döner)
    if search_query:
        feedbacks = feedbacks.filter(
            Q(raw_text__icontains=search_query) | 
            Q(service__name__icontains=search_query)
        )

    # Durum Filtresi
    if status_filter == 'processed':
        feedbacks = feedbacks.exclude(normalized_text__isnull=True).exclude(normalized_text="")
    elif status_filter == 'pending':
        feedbacks = feedbacks.filter(Q(normalized_text__isnull=True) | Q(normalized_text=""))

    # Tarih Filtreleri (Hem Admin hem Owner için)
    if start_date:
        feedbacks = feedbacks.filter(date__date__gte=parse_date(start_date))
    if end_date:
        feedbacks = feedbacks.filter(date__date__lte=parse_date(end_date))
    
    # Önem Derecesi
    if severity_filter:
        feedbacks = feedbacks.filter(severity=int(severity_filter))

    # 4. GRAFİK VERİSİ: SERVİS DAĞILIMI (Dinamik Oranlar)
    # Filtrelenmiş feedbacks üzerinden servis isimlerine göre sayım yapar
    chart_stats = feedbacks.values('service__name').annotate(count=Count('id'))
    
    labels = [item['service__name'] for item in chart_stats]
    data = [item['count'] for item in chart_stats]

    return render(request, 'feedback/dashboard.html', {
        'feedbacks': feedbacks,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'is_admin': request.user.is_superuser,
        'request': request # Filtrelerin formda seçili kalması için
    })