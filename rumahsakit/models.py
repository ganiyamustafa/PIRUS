from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
import os

class Poliklinik(models.Model):
    poliklinik = models.CharField(max_length=50, unique=True, blank=False)
    keterangan = models.TextField()

    def __str__(self):
        return self.poliklinik

    class Meta:
        ordering = ["poliklinik"]

class Fasilitas(models.Model):
    fasilitas = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.fasilitas

    class Meta:
        ordering = ["fasilitas"]

class Daerah(models.Model):
    daerah = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.daerah

    class Meta:
        ordering = ["daerah"]

class RumahSakit(models.Model):
    nama = models.CharField(max_length=50, unique=True, blank=False)
    image = models.ImageField(upload_to="img/RS/", blank=True)
    alamat = models.TextField(max_length=100, blank=False)
    no_telp = models.CharField(max_length=50,)
    deskripsi = models.TextField(blank=False)
    poliklinik = models.ManyToManyField("rumahsakit.Poliklinik", related_name='Poliklinik', blank=False, db_constraint=False)
    fasilitas = models.ManyToManyField("rumahsakit.Fasilitas", related_name='Fasilitas', blank=False, db_constraint=False)
    daerah = models.ForeignKey(Daerah, on_delete=models.PROTECT, related_name='Daerah', db_constraint=False)
    slug = models.SlugField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nama)
        super(RumahSakit, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama
    
    class Meta:
        ordering = ["nama"]

@receiver(models.signals.post_delete, sender=RumahSakit)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=RumahSakit)
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
