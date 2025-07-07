from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from videojuegos.models import SolicitudVideojuego, Videojuego


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_noob = Group.objects.get(name='Noob')
            user.groups.add(grupo_noob)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    usuario = request.user
    grupos = usuario.groups.values_list('name', flat=True)
    rol = grupos[0]

    solicitudes_enviadas = None
    solicitudes_aprobadas = None
    solicitudes_rechazadas = None
    videojuegos_creados = None

    if rol == 'Noob':
        solicitudes_enviadas = SolicitudVideojuego.objects.filter(usuario_solicitante = usuario)
        solicitudes_aprobadas = solicitudes_enviadas.filter(estado='APROB')
        solicitudes_rechazadas = solicitudes_enviadas.filter(estado='RECH')
        videojuegos_creados = Videojuego.objects.filter(usuario_creador = usuario)
    elif rol == 'Pro':
        solicitudes_aprobadas = SolicitudVideojuego.objects.filter(usuario_revisador = usuario, estado='APROB')
        solicitudes_rechazadas = SolicitudVideojuego.objects.filter(usuario_revisador = usuario, estado='RECH')
        videojuegos_creados = Videojuego.objects.filter(usuario_creador = usuario)
    context = {
        'usuario': usuario,
        'rol': rol,
        'solicitudes_enviadas': solicitudes_enviadas,
        'solicitudes_aprobadas': solicitudes_aprobadas,
        'solicitudes_rechazadas': solicitudes_rechazadas,
        'videojuegos_creados': videojuegos_creados
    }
    return render(request, 'accounts/profile.html', context)