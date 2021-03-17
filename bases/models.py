from django.db import models

from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey
from django.conf import settings


class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    um = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract=True


class ClaseModelo2(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    # uc = models.ForeignKey(User, on_delete=models.CASCADE)
    # um = models.IntegerField(blank=True,null=True)
    uc = UserForeignKey(auto_user_add=True,related_name='+')
    um = UserForeignKey(auto_user=True,related_name='+')

    class Meta:
        abstract=True

class BaseModel3(models.Model):    
    u_c = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='%(app_label)s_%(class)s_creation')
    f_c = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    u_m = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='%(app_label)s_%(class)s_updated')
    f_m = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True



# class ClaseModelo3(models.Model):
#     fc = models.DateTimeField(auto_now_add=True)
#     fm = models.DateTimeField(auto_now=True)
#     uc = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='%(app_label)s_%(class)s_creation')
#     um = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='%(app_label)s_%(class)s_updated')

#     class Meta:
#         abstract=True

class Idioma(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return self.nombre


class Frase(models.Model):
    idioma = models.ForeignKey(Idioma,on_delete=models.CASCADE)
    autor = models.CharField(max_length=50,default="Anónimo")
    frase = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Frases"

    def __str__(self):
        return "{} - {}".format(self.autor,self.idioma)