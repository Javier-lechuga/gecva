# Generated by Django 4.0.3 on 2022-11-15 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadato', '0002_xml_metadato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xml_metadato',
            name='tipo_dato',
        ),
    ]