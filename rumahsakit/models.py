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

class RegisterRumahSakit(models.Model):
    nama = models.CharField(max_length=50, unique=True, blank=False)
    alamat = models.TextField(max_length=100, blank=False)
    no_telp = models.CharField(max_length=50,)
    file_akreditansi = models.FileField(upload_to="img/RS/Register/rumahsakit/")
    is_accepted = models.BooleanField(default=False)
    is_finish_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.nama
    
    class Meta:
        ordering = ["nama"]

class RegisterHUMASRS(models.Model):
    nama = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    no_telp = models.CharField(max_length=50,)
    foto_diri = models.FileField(upload_to="img/RS/Register/humas/foto_diri/")
    foto_ktp = models.FileField(upload_to="img/RS/Register/humas/foto_ktp/")
    register_rumahsakit = models.ForeignKey(RegisterRumahSakit, related_name='register_rs', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nama
    
    class Meta:
        ordering = ["nama"]


@receiver(models.signals.post_delete, sender=RumahSakit)
def auto_delete_image_rs_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=RumahSakit)
def auto_delete_image_rs_on_change(sender, instance, **kwargs):
    if instance.image:
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

@receiver(models.signals.post_delete, sender=RegisterRumahSakit)
def auto_delete_reg_rs_image_on_delete(sender, instance, **kwargs):
    if instance.file_akreditansi:
        if os.path.isfile(instance.file_akreditansi.path):
            os.remove(instance.file_akreditansi.path)

@receiver(models.signals.pre_save, sender=RegisterRumahSakit)
def auto_delete_reg_rs_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).file_akreditansi
    except sender.DoesNotExist:
        return False
    new_file = instance.file_akreditansi
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(models.signals.post_delete, sender=RegisterHUMASRS)
def auto_delete_reg_humas_image_on_delete(sender, instance, **kwargs):
    if instance.foto_diri or instance.foto_ktp:
        if os.path.isfile(instance.foto_diri.path): os.remove(instance.foto_diri.path)
        if os.path.isfile(instance.foto_ktp.path): os.remove(instance.foto_ktp.path)

@receiver(models.signals.pre_save, sender=RegisterHUMASRS)
def auto_delete_reg_humas_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).foto_diri
        old_file2 = sender.objects.get(pk=instance.pk).foto_ktp
    except sender.DoesNotExist:
        return False
    new_file = instance.foto_diri
    new_file2 = instance.foto_ktp
    if not old_file == new_file:
        if os.path.isfile(old_file.path): os.remove(old_file.path) 
    if not old_file2 == new_file2:
        if os.path.isfile(old_file2.path): os.remove(old_file2.path)