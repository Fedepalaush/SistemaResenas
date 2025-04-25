from django.contrib import admin
from .models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('sector', 'fecha', 'amabilidad', 'eficiencia', 'limpieza')
    list_filter = ('sector', 'fecha', 'amabilidad', 'eficiencia', 'limpieza')
    search_fields = ('nombre', 'recordas_quien')
