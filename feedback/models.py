from django.db import models
from django.conf import settings # User modeli için gerekli

class Feedback(models.Model):
    # FR-9: Yapılandırılmış alanlar için seçenekler
    CATEGORY_CHOICES = [
        ('technical', 'Teknik'),
        ('service', 'Hizmet'),
        ('staff', 'Personel'),
        ('other', 'Diğer'),
    ]
    
    SEVERITY_CHOICES = [
        (1, 'Düşük'),
        (2, 'Orta'),
        (3, 'Yüksek'),
        (4, 'Kritik'),
    ]

    # FR-9 & FR-61: Ton seçenekleri
    TONE_CHOICES = [
        ('aggressive', 'Agresif'),
        ('neutral', 'Nötr'),
        ('polite', 'Nazik'),
        ('disappointed', 'Hayal Kırıklığına Uğramış'),
    ]

    # FR-9 & FR-62: Niyet seçenekleri
    INTENT_CHOICES = [
        ('complaint', 'Şikayet'),
        ('suggestion', 'Öneri'),
        ('praise', 'Övgü'),
        ('question', 'Soru'),
    ]

    # HATA 1 (User): settings.AUTH_USER_MODEL kullanarak çözüyoruz [cite: 16]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )

    # HATA 2 (Service): 'app_adi.ModelAdi' şeklinde tam yol veriyoruz [cite: 32]
    # Eğer senin servis uygulamanın klasör adı 'services' ise aşağıyı öyle güncelle:
    service = models.ForeignKey(
        'services.Service', 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )

    # Metin Alanları [cite: 30, 31, 39]
    raw_text = models.TextField(max_length=500, help_text="Orijinal şikayet metni") 
    normalized_text = models.TextField(blank=True, null=True, help_text="Düzenlenmiş metin")

    # Yapılandırılmış Veriler [cite: 29]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    severity = models.IntegerField(choices=SEVERITY_CHOICES, default=1)
    tone = models.CharField(
        max_length=20, 
        choices=TONE_CHOICES, 
        default='neutral',
        help_text="Kullanıcının algılanan tonu"
    )
    intent = models.CharField(
        max_length=20, 
        choices=INTENT_CHOICES, 
        default='complaint',
        help_text="Kullanıcının amacı"
    )
    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.id} - {self.service.name}"

    # Normalleştirme Mekanizması [cite: 37, 38]
    def save(self, *args, **kwargs):
        if not self.normalized_text:
            aggressive_words = {
                "berbat": "beklentimin altında",
                "yavaş": "hızlandırılması gereken",
                "kötü": "iyileştirilmesi gereken",
            }
            temp_text = self.raw_text.lower()
            for word, polite_word in aggressive_words.items():
                temp_text = temp_text.replace(word, polite_word)
            self.normalized_text = temp_text.capitalize()
        super().save(*args, **kwargs)