from django.shortcuts import render, redirect
from .forms import ComentarioForm
from .models import Comentario
from django.db.models import Avg
from django.contrib import messages
from datetime import date, timedelta
from datetime import datetime, date, timedelta


def dejar_comentario(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comentario_gracias')
    else:
        form = ComentarioForm()
    return render(request, 'dejar_comentario.html', {'form': form})

def comentario_gracias(request):
    return render(request, 'comentario_gracias.html')

def admin_comentarios(request):
    nombre_filtro = request.GET.get('nombre', '')

    # Obtener fechas desde GET, o asignar por defecto
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else date.today() - timedelta(days=30)
    except ValueError:
        fecha_inicio = date.today() - timedelta(days=30)

    try:
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else date.today()
    except ValueError:
        fecha_fin = date.today()

    comentarios = Comentario.objects.all()

    if nombre_filtro:
        comentarios = comentarios.filter(nombre__icontains=nombre_filtro)

    comentarios = comentarios.filter(fecha__range=[fecha_inicio, fecha_fin])
    promedio = comentarios.aggregate(Avg('calificacion'))['calificacion__avg']

    return render(request, 'admin_comentarios.html', {
        'comentarios': comentarios,
        'promedio': promedio,
        'nombre_filtro': nombre_filtro,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })