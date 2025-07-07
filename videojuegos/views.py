from django.shortcuts import render, redirect
from .models import Videojuego
from .forms import ReseñaForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    videojuegos = Videojuego.objects.prefetch_related('categorias', 'capturas').all()
    context = {
        'videojuegos': videojuegos
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