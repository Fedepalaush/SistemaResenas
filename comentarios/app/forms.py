from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'telefono', 'comentario', 'calificacion']
        widgets = {
            'calificacion': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)]),
        }
