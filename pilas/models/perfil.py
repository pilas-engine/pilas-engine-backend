from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, default="")

    class Meta:
        ordering = ['-id']
        db_table = 'perfiles'
        verbose_name_plural = "perfiles"

    class JSONAPIMeta:
        resource_name = 'perfiles'

    def __str__(self):
        return self.nombre

    @classmethod
    def crear_con_usuario(k, nombre, usuario):
        try:
            user = User.objects.get(username=usuario)
        except Exception:
            user = User.objects.create_user(username=usuario, password='123')

        user.perfil.nombre = nombre
        user.perfil.save()
        return user.perfil


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Perfil.objects.get_or_create(user=instance)
