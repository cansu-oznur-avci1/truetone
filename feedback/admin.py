from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Bu metod, admin panelinde hangi satırların görüneceğini belirler (Selection prosedürü)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Eğer kullanıcı süper kullanıcı (admin) değilse, sadece kendi servisine ait feedbackleri görsün
        if not request.user.is_superuser:
            return qs.filter(service__owner=request.user)
        return qs

    list_display = ('service', 'category', 'date', 'tone') # Tabloda görünecek sütunlar
    list_filter = ('category', 'severity') # Sağ tarafa filtreleme paneli ekler