# Generated by Django 5.2.4 on 2025-07-07 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videojuegos', '0007_alter_reseña_usuario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudvideojuego',
            name='usuario_aprobador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_aprobadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
