# Generated by Django 4.0.3 on 2022-04-01 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estatus', '0002_remove_estatus_activo_estatus_es_doc'),
        ('expediente', '0009_expediente_aprobador'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente_aprobador',
            name='id_estatus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_Estatus', to='estatus.estatus'),
        ),
    ]