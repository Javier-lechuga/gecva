# Generated by Django 4.0.3 on 2022-03-30 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('unidad', '0003_unidad_jefe_unidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unidad',
            name='jefe_unidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Jefe_unidad', to=settings.AUTH_USER_MODEL),
        ),
    ]
