from django import forms
from .models import Reseña

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