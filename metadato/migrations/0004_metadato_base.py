# Generated by Django 4.0.3 on 2022-03-30 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadato', '0003_metadato_expediente'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadato',
            name='base',
            field=models.IntegerField(default=0),
        ),
    ]