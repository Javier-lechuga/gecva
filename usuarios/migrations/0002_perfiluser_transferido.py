# Generated by Django 4.0.3 on 2022-09-12 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfiluser',
            name='transferido',
            field=models.BooleanField(default=True, verbose_name='Transferido'),
        ),
    ]
