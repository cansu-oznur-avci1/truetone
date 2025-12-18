from django.db import models
from django.conf import settings # User modeli için gerekli
from django.core.exceptions import ValidationError
import re # Düzenli ifadeler için

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

    def clean(self):
        # FR-31 & FR-64: Karakter sınırı kontrolü (500 karakter) 
        if len(self.raw_text) > 500:
            raise ValidationError("Şikayet metni 500 karakterden fazla olamaz.")
    
        # FR-12 & FR-65: Boş girişleri engelle [cite: 34, 65]
        if not self.raw_text.strip():
            raise ValidationError("Şikayet alanı boş bırakılamaz.")

    # Normalleştirme Mekanizması [cite: 37, 38]
    def save(self, *args, **kwargs):
        # FR-14: Normalleştirme süreci sadece kısa açıklama alanına uygulanır [cite: 68]
        if not self.normalized_text:
            text = self.raw_text.lower()

            # FR-35 & FR-66: Özel karakterleri ( < , > ) temizleyerek güvenliği sağla [cite: 35, 66]
            text = re.sub(r'<[^>]*?>', '', text) 
            # FR-15 & FR-69: Agresif veya duygusal ifadeleri tespit et [cite: 38, 69]
            rules = {
                r"(berbat|rezalet|iğrenç)": "beklentilerimi karşılamadı",
                r"(yavaş|kaplumbağa|bekledik)": "hızlandırılması gereken bir süreç",
                r"(kötü|çirkin)": "iyileştirilmeye açık",
                r"(ne biçim|saçma sapan|saçma)": "daha profesyonel olabilecek"
            }

            for pattern, replacement in rules.items():
                text = re.sub(pattern, replacement, text)

            # FR-70: Nazik ve nötr versiyonu oluştur [cite: 70]
            self.normalized_text = text.capitalize() 
        
        # FR-17 & FR-71: Hem ham hem de normalize metni veritabanına kaydet [cite: 39, 71]
        super().save(*args, **kwargs)