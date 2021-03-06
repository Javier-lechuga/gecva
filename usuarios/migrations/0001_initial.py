# Generated by Django 4.0.3 on 2022-03-22 17:55

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rol', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('amaterno', models.CharField(max_length=25, verbose_name='Materno')),
                ('telefono', models.CharField(max_length=25, verbose_name='Teléfono')),
                ('extension', models.CharField(max_length=25, verbose_name='Extensión')),
                ('vigente', models.BooleanField()),
                ('jefe_inmediato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Jefe_inmediato', to=settings.AUTH_USER_MODEL)),
                ('rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Rol', to='rol.rol')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
