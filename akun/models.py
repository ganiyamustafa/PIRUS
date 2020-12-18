from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save

class UserManager(BaseUserManager):
    def create_user(self, role, username, password = None):
        if not role or not username: raise ValueError("Data is not complete")
        user = self.model(role = role, username = username)
        if user.role == 'A':
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, role, username, password):
        user = self.create_user(password = password, role = role, username = username)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    ROLE = [
        ('A','Admin'),
        ('D','Direktur RS'),
    ]

    role = models.CharField(choices=ROLE, max_length=1)
    username = models.CharField(max_length=10, unique=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)    
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if self.role == 'A':
            self.is_admin = True
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'D':
            self.is_admin = False
            self.is_staff = True
            self.is_superuser = False
        super(CustomUser, self).save(*args, **kwargs)

class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='akun_admin', null=True, blank=True)
    nama = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    no_telp = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.nama

class DirekturRS(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='akun_direktur', null=True, blank=True)    
    nama = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    no_telp = models.CharField(max_length=13, unique=True)
    rumahsakit = models.ManyToManyField("rumahsakit.RumahSakit", related_name='RS', blank=False)

    def __str__(self):
        return self.nama