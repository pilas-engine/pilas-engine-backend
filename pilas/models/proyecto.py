import uuid
from django.db import models

class Proyecto(models.Model):
    hash = models.CharField(max_length=64, default="")
    nombre = models.CharField(max_length=200, default="")
    codigo = models.TextField(default="")
    codigo_serializado = models.TextField(default="")

    class Meta:
        ordering = ['-id']
        db_table = 'proyectos'
        verbose_name_plural = "proyectos"

    class JSONAPIMeta:
        resource_name = 'proyectos'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.hash = uuid.uuid4()
        super(Proyecto, self).save(*args, **kwargs)
