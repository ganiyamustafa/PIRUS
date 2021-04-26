from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
import os

class Spesialis(models.Model):
    spesialis = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.spesialis

class Doctor(models.Model):
    Jenkel_LIST = [
                ('L', 'Laki-laki'),
                ('P', 'Perempuan')
             ]

    Nama = models.CharField(max_length=100, blank=False)
    Jenkel = models.CharField(max_length=1, choices=Jenkel_LIST, blank=False)
    tgl_lahir = models.DateField(auto_now=False, auto_now_add=False, blank=False)
    image = models.ImageField(upload_to="img/dokter/", default='img/dokter/default.png', blank=True, null=True)
    pengalaman = models.CharField(max_length=3)
    pendidikan = models.CharField(max_length=100)
    rumahsakit = models.ManyToManyField("rumahsakit.RumahSakit", related_name='RumahSakit', blank=False, db_constraint=False) 
    spesialis = models.ManyToManyField("dokter.Spesialis", related_name='Spesialis', blank=False, db_constraint=False)
    slug = models.SlugField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Nama)
        super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return self.Nama

@receiver(models.signals.post_delete, sender=Doctor)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            if not 'default.png' in instance.image.path:
                os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Doctor)
def auto_delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)