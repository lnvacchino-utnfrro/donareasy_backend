# Generated by Django 3.2.6 on 2022-04-25 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DonacionesApp', '0003_alter_donacion_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bien',
            name='donacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donacion_bienes', to='DonacionesApp.donacionbienes'),
        ),
    ]
