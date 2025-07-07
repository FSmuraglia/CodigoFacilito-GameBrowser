from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('/videojuegos/<int:videojuego_id>/detail', views.detail, name="detail"),
    path('/vidojuegos/<int:videojuego_id>/añadir-reseña', views.reseña_view, name='añadir-reseña')
]