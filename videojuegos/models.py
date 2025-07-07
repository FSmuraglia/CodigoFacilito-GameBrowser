from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre

class Captura(models.Model):
    imagen = models.ImageField(null=True, blank=True, upload_to='media/videojuegos')
    videojuego = models.ForeignKey(
        'Videojuego', on_delete=models.CASCADE, related_name='capturas'
    )

    def __str__(self):
        return f"Captura de {self.videojuego.titulo}"

class Reseña(models.Model):
    videojuego = models.ForeignKey(
        'Videojuego', on_delete=models.CASCADE, related_name='reseñas'
    )
    usuario = models.ForeignKey(
        User, related_name='reseñas_usuario', on_delete=models.CASCADE
    )
    puntuacion = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    comentario = models.TextField()
    fecha_creacion = models.DateField(default=date.today)

    def __str__(self):
        return f"Reseña de {self.videojuego.titulo} por {self.usuario.username} - Puntuación: {self.puntuacion}"

class SolicitudVideojuego(models.Model):
    ESTADOS = [
        ('PEND', 'Pendiente'),
        ('APROB', 'Aprobada'),
        ('RECH', 'Rechazada')
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_solicitud = models.DateField(default=date.today)
    estado = models.CharField(max_length=5, choices=ESTADOS, default='PEND')
    categorias = models.ManyToManyField(Categoria, related_name='solicitudes')
    usuario_solicitante = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='solicitudes'
    )
    usuario_revisador = models.ForeignKey(
        User, related_name='solicitudes_aprobadas', on_delete=models.CASCADE, null=True, blank=True
    )
    año_salida = models.IntegerField(
        default=timezone.now().year,
        validators=[MinValueValidator(1950), MaxValueValidator(timezone.now().year)]
    )
    desarrollador = models.CharField(max_length=100, null=True, blank=True)
    plataformas = models.ManyToManyField('Plataforma', related_name='solicitudes')

    def __str__(self):
        return f"{self.titulo} - ({self.get_estado_display()})"
    
    class Meta:
        verbose_name_plural = 'Solicitudes de Videojuegos'

class Plataforma(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    año_salida = models.IntegerField(
        default=timezone.now().year,
        validators=[MinValueValidator(1950), MaxValueValidator(timezone.now().year)]
    )

    def __str__(self):
        return f"{self.nombre} - {self.año_salida}"

class Videojuego(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    fecha_publicacion = models.DateField(default=date.today)
    categorias = models.ManyToManyField(Categoria, related_name='videojuegos')
    descripcion = models.TextField()
    usuario_creador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='videojuegos_creados'
    )
    portada = models.OneToOneField(
        'Captura',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='portada_videojuego'
    )
    año_salida = models.IntegerField(
        default=timezone.now().year,
        validators=[MinValueValidator(1950), MaxValueValidator(timezone.now().year)]
    )
    desarrollador = models.CharField(max_length=100, null=True, blank=True)
    plataformas = models.ManyToManyField(Plataforma, related_name='videojuegos')

    def __str__(self):
        return self.titulo