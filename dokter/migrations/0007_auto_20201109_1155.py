# Generated by Django 3.1.1 on 2020-11-09 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dokter', '0006_doctor_rumahsakit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='image',
            field=models.ImageField(default='../static/img/doctor-icon.png', upload_to='img/dokter/'),
        ),
    ]
