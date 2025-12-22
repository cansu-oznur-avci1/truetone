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
        # Stil güncellemelerini koruyoruz
        if 'raw_text' in self.fields:
            self.fields['raw_text'].widget.attrs.update({
                'class': 'form-control shadow-sm rounded-4', 
            })

    def clean_raw_text(self):
        """
        Form validation for the feedback content.
        Checks for empty input and minimum character length.
        """
        # 1. Veriyi al ve başındaki/sonundaki boşlukları temizle
        raw_text = self.cleaned_data.get('raw_text', '').strip()

        # 2. Önce tamamen boş olup olmadığını kontrol et
        if not raw_text:
            raise forms.ValidationError("Feedback field cannot be empty.")
            
        # 3. Boş değilse, uzunluğunu kontrol et
        if len(raw_text) < 10:
            raise forms.ValidationError("Please provide more detail about your experience. (Minimum 10 characters required)")
            
        return raw_text