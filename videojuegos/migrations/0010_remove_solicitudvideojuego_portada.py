# Generated by Django 5.2.4 on 2025-07-07 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videojuegos', '0009_solicitudvideojuego_año_salida_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudvideojuego',
            name='portada',
        ),
    ]
