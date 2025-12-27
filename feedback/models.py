from django.db import models
from django.conf import settings # User modeli için gerekli
from django.core.exceptions import ValidationError
import re # Düzenli ifadeler için

class Feedback(models.Model):
    # FR-9: Yapılandırılmış alanlar için seçenekler
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('service', 'Service'),
        ('staff', 'Staff'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]

    # FR-9 & FR-61: Ton seçenekleri
    TONE_CHOICES = [
        ('aggressive', 'Aggressive'),
        ('neutral', 'Neutral'),
        ('polite', 'Polite'),
        ('disappointed', 'Disappointed'),
    ]
    # FR-9 & FR-62: Niyet seçenekleri
    INTENT_CHOICES = [
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('praise', 'Praise'),
        ('question', 'Question'),
    ]

    # HATA 1 (User): settings.AUTH_USER_MODEL kullanarak çözüyoruz [cite: 16]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )

    # HATA 2 (Service): 'app_adi.ModelAdi' şeklinde tam yol veriyoruz [cite: 32]
    service = models.ForeignKey(
        'services.Service', 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )

    # Metin Alanları [cite: 30, 31, 39]
    raw_text = models.TextField(max_length=500, help_text="Original feedback text") 
    normalized_text = models.TextField(blank=True, null=True, help_text="Normalized text")

    # Yapılandırılmış Veriler [cite: 29]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    severity = models.IntegerField(choices=SEVERITY_CHOICES, default=1)
    tone = models.CharField(
        max_length=20, 
        choices=TONE_CHOICES, 
        help_text="Detected user tone"
    )
    intent = models.CharField(
        max_length=20, 
        choices=INTENT_CHOICES, 
        help_text="Detected user intent"
    )
    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.id} - {self.service.name}"

    def clean(self):
        # FR-31 & FR-64: Karakter sınırı kontrolü (500 karakter) 
        if len(self.raw_text) > 500:
            raise ValidationError("Feedback text cannot exceed 500 characters.")
    
        # FR-12 & FR-65: Boş girişleri engelle [cite: 34, 65]
        if not self.raw_text.strip():
            raise ValidationError("Feedback field cannot be empty.")

    # Normalleştirme Mekanizması [cite: 37, 38]
    def save(self, *args, **kwargs):
        # FR-14: Normalleştirme süreci sadece kısa açıklama alanına uygulanır [cite: 68]
        # Eğer birisi manuel bir normalized_text göndermemişse 
        # (yani AI henüz çalışmamışsa) varsayılan olarak raw_text atayabiliriz.
        if not self.normalized_text:
            self.normalized_text = self.raw_text
            
        super().save(*args, **kwargs)