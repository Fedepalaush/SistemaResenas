from django import forms
from .models import Comentario

# Diccionario con personal por sector
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
        super().__init__(*args, **kwargs)

        # Establecer widgets para las calificaciones (RadioSelect)
        self.fields['amabilidad'].widget = forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        self.fields['eficiencia'].widget = forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        self.fields['limpieza'].widget = forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])

        # Si el sector fue enviado, actualizamos las opciones de 'recordas_quien'
        sector = self.initial.get('sector')  # El valor de 'sector' debería estar en initial
        if sector and sector in PERSONAL_POR_SECTOR:
            choices = [('', '---------')] + [(p, p) for p in PERSONAL_POR_SECTOR[sector]]
            self.fields['recordas_quien'].widget = forms.Select(choices=choices)
        else:
            choices = [('', 'No disponible')]
            self.fields['recordas_quien'].widget = forms.Select(choices=choices)

    # Validación de los campos 'amabilidad', 'eficiencia' y 'limpieza'
    def clean_amabilidad(self):
        amabilidad = self.cleaned_data.get('amabilidad')
        if not amabilidad:
            raise forms.ValidationError("Seleccione un valor del 1 al 5")
        return amabilidad

    def clean_eficiencia(self):
        eficiencia = self.cleaned_data.get('eficiencia')
        if not eficiencia:
            raise forms.ValidationError("Seleccione un valor del 1 al 5")
        return eficiencia

    def clean_limpieza(self):
        limpieza = self.cleaned_data.get('limpieza')
        if not limpieza:
            raise forms.ValidationError("Seleccione un valor del 1 al 5")
        return limpieza
