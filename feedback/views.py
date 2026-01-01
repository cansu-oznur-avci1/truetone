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
    service = get_object_or_404(Service, id=service_id) 
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user 
            feedback.service = service 
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
    return render(request, 'feedback/submit_feedback.html', {'form': form, 'service': service})

@login_required
def user_feedback_list(request):
    query_set = Feedback.objects.filter(user=request.user).order_by('-date')
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    severity_filter = request.GET.get('severity', '')
    if search_query:
        query_set = query_set.filter(
            Q(raw_text__icontains=search_query) | 
            Q(normalized_text__icontains=search_query)
        )
    
    if status_filter:
        if status_filter == 'processed':
            query_set = query_set.exclude(normalized_text__isnull=True).exclude(normalized_text__exact='')
        elif status_filter == 'pending':
            query_set = query_set.filter(Q(normalized_text__isnull=True) | Q(normalized_text__exact=''))

    if severity_filter:
        query_set = query_set.filter(severity=int(severity_filter))

    total_sent = query_set.count()
    processed_count = query_set.exclude(normalized_text__isnull=True).exclude(normalized_text__exact='').count()

    # context içine 'request' ekleyerek veya parametreleri tek tek göndererek 
    # HTML'de seçili kalmalarını sağlıyoruz.
    return render(request, 'feedback/user_feedback_list.html', {
        'feedbacks': query_set, 
        'total_sent': total_sent,
        'processed_count': processed_count
    })

@login_required
def service_owner_dashboard(request):
    """Cansu'nun belirttiği aynı isimli servisleri ayırma sorunu burada çözüldü"""
    all_services = Service.objects.all() if request.user.is_superuser else None
    # 1. Yetki Kontrolü (Korundu)
    if request.user.is_superuser:
        feedbacks = Feedback.objects.all().order_by('-date')
    elif request.user.managed_services.exists():
        feedbacks = Feedback.objects.filter(service__owner=request.user).order_by('-date')
    else:
        return redirect('home')

    # 2. Filtreler (Korundu)
    q = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    severity_f = request.GET.get('severity', '')
    service_id_f = request.GET.get('service_filter', '')

    if q:
        feedbacks = feedbacks.filter(Q(raw_text__icontains=q) | Q(service__name__icontains=q))
    if start_date:
        feedbacks = feedbacks.filter(date__date__gte=parse_date(start_date))
    if end_date:
        feedbacks = feedbacks.filter(date__date__lte=parse_date(end_date))
    if severity_f:
        feedbacks = feedbacks.filter(severity=int(severity_f))
    if service_id_f:
        feedbacks = feedbacks.filter(service_id=service_id_f)

    # 3. Dinamik Grafik Mantığı 
    # Koşul: Eğer bir servis seçilmişse VEYA kullanıcı Service Owner ise -> SEVERITY GÖSTER
    if service_id_f or not request.user.is_superuser:
        chart_stats = feedbacks.values('severity').annotate(count=Count('id')).order_by('severity')
        labels = [f"Level {item['severity']}" for item in chart_stats]
        chart_title = "Severity Level Distribution"
    
    # Koşul: Admin henüz servis seçmemişse -> SERVİS DAĞILIMI GÖSTER
    else:
        # Admin Genel Bakış: Servisleri sadece isimlerine göre gruplayıp sayılarını topluyoruz
        chart_stats = feedbacks.values('service__name').annotate(count=Count('id')).order_by('-count')
        
        # Etiketleri (Service Names) hazırlıyoruz
        labels = [item['service__name'] for item in chart_stats]
        chart_title = "Global Service Feedback Distribution"

    data = [item['count'] for item in chart_stats]

    return render(request, 'feedback/dashboard.html', {
        'feedbacks': feedbacks,
        'all_services': all_services, 
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'chart_title': chart_title,
        'is_admin': request.user.is_superuser,
        'request': request
    })