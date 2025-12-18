from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm

@login_required # FR-19 & FR-89: Sadece giriş yapanlar feedback verebilir
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user # Şikayeti yapan kullanıcıyı set et
            feedback.save() # Burada senin yazdığın Normalizer otomatik çalışacak! (FR-17)
            return render(request, 'feedback/success.html', {'feedback': feedback})
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit_feedback.html', {'form': form})

