# Generated by Django 4.0.3 on 2022-03-17 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expediente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='motivo_rechazo',
            field=models.CharField(max_length=245, verbose_name='motivo_rechazo'),
        ),
    ]
