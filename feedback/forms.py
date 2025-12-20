from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        
        fields = ['category', 'severity', 'tone', 'intent', 'raw_text'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
       
        self.fields['raw_text'].widget = forms.Textarea(attrs={
            'placeholder': 'Explain your issue briefly...',
            'rows': 3,
            'class': 'form-control',
            'maxlength': '150' 
        })

        
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['severity'].widget.attrs.update({'class': 'form-select'})
        self.fields['tone'].widget.attrs.update({'class': 'form-select'})
        self.fields['intent'].widget.attrs.update({'class': 'form-select'})