# Generated by Django 2.2.8 on 2021-03-06 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumahsakit', '0009_auto_20210306_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerrumahsakit',
            name='is_accepted',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registerrumahsakit',
            name='is_finish_registered',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]