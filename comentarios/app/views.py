from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import ComentarioForm
from .models import Comentario


def dejar_comentario(request, sector):
    print(f"Sector recibido: {sector}")

    if request.method == 'POST':
        # Imprime los datos que se están enviando en el POST
        print(f"Datos enviados en el POST: {request.POST}")

        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.sector = sector
            comentario.save()

            # Marcar el sector como votado en la sesión
            sectores_votados = request.session.get('sectores_votados', [])
            if sector not in sectores_votados:
                sectores_votados.append(sector)
                request.session['sectores_votados'] = sectores_votados

            return redirect('comentario_gracias')
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = ComentarioForm(initial={'sector': sector})

    return render(request, 'dejar_comentario.html', {'form': form, 'sector': sector})


def comentario_gracias(request):
    """Vista de agradecimiento luego de dejar un comentario."""
    return render(request, 'comentario_gracias.html')


def administrar_comentarios(request):
    """Vista para administrar los comentarios: filtros, estadísticas, listados y paginación."""
    hoy = date.today()
    un_mes_atras = hoy - timedelta(days=30)

    # Filtros del request (o valores por defecto)
    nombre_filtro = request.GET.get('nombre', '')
    fecha_inicio = request.GET.get('fecha_inicio') or un_mes_atras.strftime('%Y-%m-%d')
    fecha_fin = request.GET.get('fecha_fin') or hoy.strftime('%Y-%m-%d')
    sector_filtro = request.GET.get('sector', '')

    # Base queryset
    comentarios = Comentario.objects.all()

    # Aplicar filtros
    if nombre_filtro:
        comentarios = comentarios.filter(nombre__icontains=nombre_filtro)
    if fecha_inicio:
        comentarios = comentarios.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        comentarios = comentarios.filter(fecha__lte=fecha_fin)
    if sector_filtro:
        comentarios = comentarios.filter(sector=sector_filtro)

    # Calcular promedios
    promedios = comentarios.aggregate(
        amabilidad_avg=Avg('amabilidad'),
        eficiencia_avg=Avg('eficiencia'),
        limpieza_avg=Avg('limpieza')
    )

    # Agrupar recordatorios y cómo conocieron
    recordas_quien_hist = list(
        comentarios.values('recordas_quien')
        .annotate(count=Count('recordas_quien'))
        .order_by('recordas_quien')
    )

    como_conociste_hist = list(
        comentarios.values('como_conociste')
        .annotate(count=Count('como_conociste'))
        .order_by('como_conociste')
    )

    # Opciones posibles de sector
    SECTORES_POSIBLES = ['fiambreria', 'carniceria', 'salon', 'caja']
    sectores = sorted(SECTORES_POSIBLES)

    # Paginación
    paginator = Paginator(comentarios,20)  # 10 comentarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_comentarios.html', {
        'nombre_filtro': nombre_filtro,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'sector_filtro': sector_filtro,
        'page_obj': page_obj,
        'promedios': promedios,
        'recordas_quien_hist': recordas_quien_hist,
        'como_conociste_hist': como_conociste_hist,
        'sectores': sectores,
    })


def elegir_sector(request):
    sectores_votados = request.session.get('sectores_votados', [])

    if request.method == 'POST':
        sector = request.POST.get('sector')
        if sector in sectores_votados:
            # Ya votó este sector, no hacer nada o mostrar un mensaje
            return redirect('elegir_sector')
        else:
            return redirect('dejar_comentario', sector=sector)

    return render(request, 'elegir_sector.html', {'sectores_votados': sectores_votados})


