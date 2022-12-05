# Generated by Django 3.2.6 on 2022-09-07 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0006_delete_chicos'),
        ('ApadrinamientoApp', '0003_auto_20220731_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudapadrinamiento',
            name='institucion',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='baseApp.institucion', verbose_name='institucion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitudapadrinamiento',
            name='chico_apadrinado',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chico_apadrinado', to='ApadrinamientoApp.chicos', verbose_name='chico'),
        ),
    ]