# Generated by Django 5.2.4 on 2025-07-07 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videojuegos', '0002_alter_solicitudvideojuego_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='videojuego',
            name='portada',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='portada_videojuego', to='videojuegos.captura'),
        ),
    ]
