from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from services.models import Service 
from .forms import FeedbackForm

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