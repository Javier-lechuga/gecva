# Generated by Django 4.0.3 on 2022-11-15 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadato', '0003_remove_xml_metadato_tipo_dato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xml_metadato',
            name='metadato',
        ),
    ]
