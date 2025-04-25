from django.db import models

class Comentario(models.Model):
    SECTOR_CHOICES = [
        ('carniceria', 'Carnicería'),
        ('fiambreria', 'Fiambrería'),
        ('salon', 'Salón'),
        ('caja', 'Caja'),
    ]

    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    nombre = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    amabilidad = models.IntegerField()
    eficiencia = models.IntegerField()
    limpieza = models.IntegerField()
    recordas_quien = models.CharField(max_length=100, blank=True)
    destacado = models.TextField(blank=True)

    como_conociste = models.CharField(max_length=50, choices=[
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('google', 'Google'),
        ('pantallas', 'Pantallas'),
        ('recomendacion', 'Recomendación'),
    ])

    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_sector_display()} ({self.fecha})"
