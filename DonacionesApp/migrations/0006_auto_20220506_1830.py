# Generated by Django 3.2.6 on 2022-05-06 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DonacionesApp', '0005_auto_20220429_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='donacion',
            name='fecha_cancelacion',
            field=models.DateTimeField(blank=True, null=True, verbose_name='fecha_cancelacion'),
        ),
        migrations.AddField(
            model_name='donacion',
            name='motivo_cancelacion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='descripcion'),
        ),
    ]
