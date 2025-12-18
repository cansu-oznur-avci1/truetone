from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        # Kullanıcının dolduracağı alanlar (FR-9, FR-10)
        fields = ['service', 'category', 'severity', 'tone', 'intent', 'raw_text']
        # Görünümü güzelleştirmek için widget ekliyoruz
        widgets = {
            'raw_text': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Şikayetinizi buraya yazın...', 
                'rows': 4
            }),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'tone': forms.Select(attrs={'class': 'form-select'}),
            'intent': forms.Select(attrs={'class': 'form-select'}),
        }