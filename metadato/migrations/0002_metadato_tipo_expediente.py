# Generated by Django 4.0.3 on 2022-03-22 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_expediente', '0001_initial'),
        ('metadato', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadato',
            name='tipo_expediente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tipo_exp', to='tipo_expediente.tipoexpediente'),
        ),
    ]
