from django.shortcuts import render, redirect
from .models import Videojuego, Captura, SolicitudVideojuego, Categoria, Plataforma
from .forms import ReseñaForm, VideojuegoForm, SolicitudVideojuegoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

def es_pro_o_admin(user):
    return user.is_authenticated and user.groups.filter(name__in=['Pro', 'Admin']).exists()

def es_noob(user):
    return user.is_authenticated and user.groups.filter(name='Noob').exists()

# Create your views here.
def index(request):
    videojuegos = Videojuego.objects.prefetch_related('categorias', 'capturas').all()
    titulo = request.GET.get('titulo', '')
    categorias = request.GET.getlist('categorias')
    plataformas = request.GET.getlist('plataformas')
    año_desde = request.GET.get('año_desde')
    año_hasta = request.GET.get('año_hasta')

    if titulo:
        videojuegos = videojuegos.filter(titulo__icontains=titulo)
    if categorias:
        videojuegos = videojuegos.filter(categorias__id__in=categorias).distinct()
    if plataformas:
        videojuegos = videojuegos.filter(plataformas__id__in=plataformas).distinct()
    if año_desde:
        videojuegos = videojuegos.filter(año_salida__gte=año_desde)
    if año_hasta:
        videojuegos = videojuegos.filter(año_salida__lte=año_hasta)
    
    todas_las_categorias = Categoria.objects.all()
    todas_las_plataformas = Plataforma.objects.all()

    context = {
        'videojuegos': videojuegos,
        'todas_las_categorias': todas_las_categorias,
        'todas_las_plataformas': todas_las_plataformas,
        'categorias_seleccionadas': categorias,
        'plataformas_seleccionadas': plataformas
    }

    return render(request, 'videojuegos/index.html', context)

def detail(request, videojuego_id):
    videojuego = Videojuego.objects.prefetch_related('categorias', 'capturas', 'reseñas').get(id=videojuego_id)
    reseñas = videojuego.reseñas.all().order_by('-fecha_creacion')
    form = ReseñaForm()

    context = {
        'videojuego': videojuego,
        'app_name': videojuego.titulo,
        'form': form,
        'reseñas': reseñas
    }

    return render(request, 'videojuegos/detail.html', context)

@login_required
def reseña_view(request, videojuego_id):
    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            user = request.user
            nueva_reseña = form.save(commit=False)
            nueva_reseña.usuario = user
            nueva_reseña.videojuego = Videojuego.objects.get(id=videojuego_id)
            nueva_reseña.save()

    return redirect('detail', videojuego_id=videojuego_id)

@login_required
@user_passes_test(es_pro_o_admin)
def crear_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            videojuego = form.save(commit=False)
            videojuego.usuario_creador = request.user
            videojuego.save()
            form.save_m2m()

            portada = Captura.objects.create(
                imagen = form.cleaned_data['portada'],
                videojuego = videojuego
            )
            videojuego.portada = portada
            videojuego.save()

            for imagen in request.FILES.getlist('capturas_adicionales'):
                Captura.objects.create(
                    imagen = imagen,
                    videojuego = videojuego
                )
            return redirect('detail', videojuego_id=videojuego.id)
    else:
        form = VideojuegoForm()
        
    return render(request, 'videojuegos/crear_videojuego.html', {'form': form})

@login_required
@user_passes_test(es_noob)
def enviar_solicitud_videojuego(request):
    if request.method == 'POST':
        form = SolicitudVideojuegoForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario_solicitante = request.user
            solicitud.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = SolicitudVideojuegoForm()
    
    return render(request, 'videojuegos/solicitud_videojuego.html', {'form':form})

@login_required
@user_passes_test(es_pro_o_admin)
def listar_solicitudes(request):
    solicitudes = SolicitudVideojuego.objects.filter(estado='PEND')
    context = {
        'solicitudes': solicitudes
    }

    return render(request, 'videojuegos/listar_solicitudes.html', context)

@login_required
@user_passes_test(es_pro_o_admin)
def revisar_solicitud(request, solicitud_id):
    solicitud = SolicitudVideojuego.objects.get(id=solicitud_id)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aprobar':
            solicitud.estado = 'APROB'
            solicitud.usuario_revisador = request.user
            solicitud.save()

            videojuego = Videojuego.objects.create(
                titulo = solicitud.titulo,
                descripcion = solicitud.descripcion,
                usuario_creador = solicitud.usuario_solicitante,
                año_salida = solicitud.año_salida,
                desarrollador = solicitud.desarrollador
            )
            videojuego.categorias.set(solicitud.categorias.all())
            videojuego.plataformas.set(solicitud.plataformas.all())

            cantidad_aprobados = Videojuego.objects.filter(usuario_creador=solicitud.usuario_solicitante).count()
            if cantidad_aprobados >=5:
                grupo_pro = Group.objects.get(name='Pro')
                solicitud.usuario_solicitante.groups.clear()
                solicitud.usuario_solicitante.groups.add(grupo_pro)
            
            return redirect('listar-solicitudes')
        elif accion == 'rechazar':
            solicitud.estado = 'RECH'
            solicitud.usuario_revisador = request.user
            solicitud.save()

            return redirect('listar-solicitudes')
    
    return render(request, 'videojuegos/revisar_solicitud.html', {'solicitud': solicitud})

@login_required
@user_passes_test(es_pro_o_admin)
def editar_videojuego(request, videojuego_id):
    videojuego = Videojuego.objects.get(id=videojuego_id)

    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES, instance=videojuego)
        if form.is_valid():
            videojuego = form.save()

            if 'portada' in request.FILES:
                nueva_captura = Captura.objects.create(
                    imagen = form.cleaned_data['portada'],
                    videojuego = videojuego
                )
                videojuego.portada = nueva_captura
                videojuego.save()
            
            for imagen in request.FILES.getlist('capturas_adicionales'):
                Captura.objects.create(imagen = imagen, videojuego = videojuego)
            
            return redirect('detail', videojuego_id=videojuego.id)
    else:
        form = VideojuegoForm(instance=videojuego)
    
    context = {
        'form': form,
        'videojuego': videojuego
    }

    return render(request, 'videojuegos/editar_videojuego.html', context)

@login_required
@user_passes_test(es_pro_o_admin)
def eliminar_videojuego(request, videojuego_id):
    videojuego = Videojuego.objects.get(id=videojuego_id)
    videojuego.delete()
    return redirect('index')