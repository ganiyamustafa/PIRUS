# Generated by Django 2.2.8 on 2021-03-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumahsakit', '0010_auto_20210306_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerrumahsakit',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registerrumahsakit',
            name='is_finish_registered',
            field=models.BooleanField(default=False),
        ),
    ]
