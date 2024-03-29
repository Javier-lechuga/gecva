# Generated by Django 4.0.3 on 2022-11-15 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_dato', '0001_initial'),
        ('expediente', '0004_expediente_aprobador_activo'),
        ('metadato', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='xml_metadato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_xml', models.DateTimeField(null=True, verbose_name='fecha_xml')),
                ('folio', models.CharField(max_length=245, null=True, verbose_name='folio_xml')),
                ('cond_pago', models.CharField(max_length=245, null=True, verbose_name='pago_xml')),
                ('moneda', models.CharField(max_length=245, null=True, verbose_name='moneda_xml')),
                ('tipo_comprobante', models.CharField(max_length=245, null=True, verbose_name='comprobante_xml')),
                ('metodo_pago', models.CharField(max_length=245, null=True, verbose_name='metodo_xml')),
                ('lugar_exp', models.CharField(max_length=245, null=True, verbose_name='lugar_xml')),
                ('subtotal', models.CharField(max_length=245, null=True, verbose_name='subtotal_xml')),
                ('descuento', models.CharField(max_length=245, null=True, verbose_name='descuento_xml')),
                ('total', models.CharField(max_length=245, null=True, verbose_name='total_xml')),
                ('rfc_emisor', models.CharField(max_length=245, null=True, verbose_name='rfc_emisor_xml')),
                ('nombre_emisor', models.CharField(max_length=245, null=True, verbose_name='nombre_emisor_xml')),
                ('regimen_fiscal_emisor', models.CharField(max_length=245, null=True, verbose_name='regimen_emisor_xml')),
                ('rfc_receptor', models.CharField(max_length=245, null=True, verbose_name='rfc_receptor_xml')),
                ('nombre_receptor', models.CharField(max_length=245, null=True, verbose_name='nombre_receptor_xml')),
                ('regimen_fiscal_receptor', models.CharField(max_length=245, null=True, verbose_name='regimen_receptor_xml')),
                ('expediente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expediente_xml', to='expediente.expediente')),
                ('metadato', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Metadato_xml', to='metadato.metadato')),
                ('tipo_dato', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tipo_dato_xml', to='tipo_dato.tipodato')),
            ],
        ),
    ]
