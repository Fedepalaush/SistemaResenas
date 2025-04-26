from django.urls import path
from . import views

urlpatterns = [
    path('dejar-comentario/<str:sector>/', views.dejar_comentario, name='dejar_comentario'),
    path('gracias/', views.comentario_gracias, name='comentario_gracias'),
    path('administrar/', views.administrar_comentarios, name='admin_comentarios'),
    path('elegir-sector/', views.elegir_sector, name='elegir_sector'),
]
