from django.db import models
from django.conf import settings

class Service(models.Model):
    SERVICE_CATEGORIES = [
        ('education', 'Eğitim'),
        ('food', 'Beslenme/Yemek'),
        ('facility', 'Tesis/Altyapı'),
        ('it', 'Bilgi İşlem'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_services'
    )

    def __str__(self):
        return self.name

