# Generated by Django 2.2.8 on 2021-01-10 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dokter', '0008_auto_20201109_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='image',
            field=models.ImageField(blank=True, default='img/dokter/default.png', null=True, upload_to='img/dokter/'),
        ),
    ]
