from django.shortcuts import render
from django.http import HttpResponse
from .models import Videojuego

# Create your views here.
def index(request):
    videojuegos = Videojuego.objects.prefetch_related('categorias', 'capturas').all()
    context = {
        'videojuegos': videojuegos
    }

    return render(request, 'videojuegos/index.html', context)