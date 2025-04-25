from django.urls import path
from . import views

urlpatterns = [
    path('dejar-comentario/', views.dejar_comentario, name='dejar_comentario'),
    path('gracias/', views.comentario_gracias, name='comentario_gracias'),
    path('administrar/', views.admin_comentarios, name='admin_comentarios'),
]
