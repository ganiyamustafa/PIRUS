# Generated by Django 2.2.8 on 2021-03-07 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rumahsakit', '0013_auto_20210307_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerhumasrs',
            name='register_rumahsakit',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='register_rs', to='rumahsakit.RegisterRumahSakit'),
        ),
    ]
