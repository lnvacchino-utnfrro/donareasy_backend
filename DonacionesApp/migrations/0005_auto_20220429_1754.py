# Generated by Django 3.2.6 on 2022-04-29 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DonacionesApp', '0004_alter_bien_donacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bien',
            name='donacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bienes', to='DonacionesApp.donacionbienes'),
        ),
        migrations.AlterField(
            model_name='donacion',
            name='fecha_aceptacion',
            field=models.DateTimeField(blank=True, null=True, verbose_name='fecha_aceptacion'),
        ),
    ]
