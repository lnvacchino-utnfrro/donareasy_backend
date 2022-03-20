# Generated by Django 3.2.6 on 2022-01-26 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donante',
            name='edad',
        ),
        migrations.RemoveField(
            model_name='donante',
            name='email',
        ),
        migrations.AddField(
            model_name='donante',
            name='dni',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='dni'),
        ),
        migrations.AddField(
            model_name='donante',
            name='domicilio',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='domicilio'),
        ),
        migrations.AddField(
            model_name='donante',
            name='estado_civil',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='provincia'),
        ),
        migrations.AddField(
            model_name='donante',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='fecha_nacimiento'),
        ),
        migrations.AddField(
            model_name='donante',
            name='genero',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='genero'),
        ),
        migrations.AddField(
            model_name='donante',
            name='localidad',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ciudad'),
        ),
        migrations.AddField(
            model_name='donante',
            name='ocupacion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ocupacion'),
        ),
        migrations.AddField(
            model_name='donante',
            name='pais',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='pais'),
        ),
        migrations.AddField(
            model_name='donante',
            name='provincia',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='provincia'),
        ),
        migrations.AddField(
            model_name='donante',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='telefono'),
        ),
        migrations.AddField(
            model_name='donante',
            name='usuario',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL, verbose_name='id_usuario'),
        ),
        migrations.AlterField(
            model_name='donante',
            name='apellido',
            field=models.CharField(blank=True, max_length=100, verbose_name='apellido'),
        ),
        migrations.AlterField(
            model_name='donante',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, verbose_name='nombre'),
        ),
    ]
