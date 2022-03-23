# Generated by Django 4.0.3 on 2022-03-22 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_expediente', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expediente', '0006_alter_expediente_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='usuario_crea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_crea', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='tipo_expediente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tipo_expediente', to='tipo_expediente.tipoexpediente'),
        ),
    ]