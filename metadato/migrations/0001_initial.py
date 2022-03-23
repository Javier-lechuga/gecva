# Generated by Django 4.0.3 on 2022-03-17 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estatus', '0002_remove_estatus_activo_estatus_es_doc'),
        ('tipo_dato', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metadato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=245, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=245, null=True, verbose_name='Descripción')),
                ('obligatorio', models.BooleanField(default=False, verbose_name='Obligatorio')),
                ('valor', models.CharField(max_length=245, verbose_name='Valor')),
                ('version', models.CharField(max_length=245, null=True, verbose_name='Versión')),
                ('motivo_rechazo', models.CharField(max_length=245, null=True, verbose_name='Motivo_rechazo')),
                ('estatus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estatus_uno', to='estatus.estatus')),
                ('tipo_dato', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tipo_dato', to='tipo_dato.tipodato')),
            ],
        ),
    ]