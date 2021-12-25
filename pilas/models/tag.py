import os
import zipfile
import uuid
import shutil
from django.db import models
from django.core.files import File


class Tag(models.Model):
    nombre = models.CharField(max_length=128, default="")
    creacion = models.DateTimeField(auto_now_add=True, null=True)

    # Relaciones inversas:
    #
    # proyectos (manyToMany)

    class Meta:
        ordering = ['-id']
        db_table = 'tags'
        verbose_name_plural = "tags"

    def __str__(self):
        return self.nombre
