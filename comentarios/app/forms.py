from django import forms
from .models import Comentario

PERSONAL_POR_SECTOR = {
    'carniceria': ['Seba', 'Tanty', 'Nahuel', 'Sandra', 'Ema', 'Jorge'],
    'caja': ['Noe', 'Jesa', 'Maxi', 'Marce'],
    'fiambreria': ['Omar', 'Maxi', 'Milli', 'Marce'],
    'salon': ['Omar', 'Maxi', 'Milli', 'Marce'],
}

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = [
            'sector', 'nombre', 'telefono',
            'amabilidad', 'eficiencia', 'limpieza',
            'recordas_quien', 'destacado',
            'como_conociste'
        ]

    def __init__(self, *args, **kwargs):
        # Obtenemos el sector desde initial o data
        sector = kwargs.get('initial', {}).get('sector') or kwargs.get('data', {}).get('sector')
        
        super().__init__(*args, **kwargs)

        # Establecemos los widgets de las calificaciones
        self.fields['amabilidad'].widget = forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        self.fields['eficiencia'].widget = forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        self.fields['limpieza'].widget = forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        
        # Verificamos el sector y actualizamos las opciones para el campo recordas_quien
        if sector in PERSONAL_POR_SECTOR:
            choices = [('', '---------')] + [(p, p) for p in PERSONAL_POR_SECTOR[sector]]
            self.fields['recordas_quien'].widget = forms.Select(choices=choices)
        else:
            self.fields['recordas_quien'].widget = forms.TextInput(attrs={'placeholder': '¿Recordás quién te atendió?'})

