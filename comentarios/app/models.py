from django.db import models

CALIFICACIONES = [(i, f"{i} estrella{'s' if i > 1 else ''}") for i in range(1, 6)]

class Comentario(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    comentario = models.TextField(blank=True)
    calificacion = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)  # <-- Campo nuevo

    def __str__(self):
        return f"{self.nombre} ({self.calificacion}★)"
