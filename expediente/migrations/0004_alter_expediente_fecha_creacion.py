# Generated by Django 4.0.3 on 2022-03-17 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expediente', '0003_remove_expediente_usuario_crea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='fecha_creacion',
            field=models.DateTimeField(null=True, verbose_name='Creación'),
        ),
    ]
