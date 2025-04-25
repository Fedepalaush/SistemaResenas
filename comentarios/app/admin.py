from django.contrib import admin
from .models import Comentario  # Importá el modelo

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'comentario', 'calificacion', 'fecha')
    list_filter = ('calificacion', 'fecha')
    search_fields = ('nombre', 'comentario')
