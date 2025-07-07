from django.contrib import admin
from .models import Categoria, Captura, Reseña, SolicitudVideojuego, Videojuego, Plataforma

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Captura)
admin.site.register(Reseña)
admin.site.register(SolicitudVideojuego)
admin.site.register(Videojuego)
admin.site.register(Plataforma)