# Generated by Django 3.2.6 on 2023-09-21 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0008_institucion_habilitado'),
    ]

    operations = [
        migrations.AddField(
            model_name='institucion',
            name='codigo_habilitacion',
            field=models.CharField(blank=True, default='16f644780f2ad8e014cd', max_length=20, verbose_name='codigo_habilitacion'),
        ),
    ]
