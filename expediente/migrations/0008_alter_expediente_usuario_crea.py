# Generated by Django 4.0.3 on 2022-03-22 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expediente', '0007_expediente_usuario_crea_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='usuario_crea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
