from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('videojuegos/<int:videojuego_id>/detail', views.detail, name="detail"),
    path('videojuegos/<int:videojuego_id>/añadir-reseña', views.reseña_view, name='añadir-reseña'),
    path('videojuegos/crear', views.crear_videojuego, name='crear-videojuego'),
    path('videojuegos/solicitud/', views.enviar_solicitud_videojuego, name='solicitud-videojuego'),
    path('videojuegos/solicitudes/', views.listar_solicitudes, name='listar-solicitudes'),
    path('videojuegos/solicitudes/<int:solicitud_id>', views.revisar_solicitud, name='revisar-solicitud')
]