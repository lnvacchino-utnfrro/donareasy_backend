# Generated by Django 3.2.6 on 2022-06-23 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recoleccion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recoleccion',
            name='fecha_recoleccion',
            field=models.DateField(blank=True, null=True, verbose_name='fecha_recoleccion'),
        ),
        migrations.AddField(
            model_name='recoleccion',
            name='hora_recoleccion',
            field=models.TimeField(blank=True, null=True, verbose_name='hora_recoleccion'),
        ),
    ]