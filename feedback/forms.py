from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['raw_text'] 
        widgets = {
            'raw_text': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Explain your issue briefly (e.g., The library was very quiet and productive today)...',
                'rows': 4,
                'maxlength': '500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sadece mevcut alanlar için özellikleri güncelle
        if 'raw_text' in self.fields:
            self.fields['raw_text'].widget.attrs.update({
                'class': 'form-control shadow-sm rounded-3',
            })