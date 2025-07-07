from django import forms
from .models import Reseña, Videojuego

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['puntuacion', 'comentario']
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5, 'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'puntuacion': 'Puntuación (1 a 5)',
            'comentario': 'Comentario',
        }

class VideojuegoForm(forms.ModelForm):
    portada = forms.ImageField(required=True)

    class Meta:
        model = Videojuego
        fields = ['titulo', 'descripcion', 'año_salida', 'desarrollador', 'categorias', 'plataformas']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'año_salida': forms.NumberInput(attrs={'class': 'form-control'}),
            'desarrollador': forms.TextInput(attrs={'class': 'form-control'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'plataformas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }