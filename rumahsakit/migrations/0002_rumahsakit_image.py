# Generated by Django 3.1.1 on 2020-09-07 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumahsakit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rumahsakit',
            name='image',
            field=models.ImageField(default=1, upload_to='img/RS/'),
            preserve_default=False,
        ),
    ]