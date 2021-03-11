import uuid
from django.db import models
import zipfile

class Proyecto(models.Model):
    hash = models.CharField(max_length=64, default="")
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    ver_codigo = models.BooleanField(default=True)
    archivo = models.FileField(upload_to='proyectos/', default=None, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'proyectos'
        verbose_name_plural = "proyectos"

    class JSONAPIMeta:
        resource_name = 'proyectos'

    def __str__(self):
        return self.hash

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = uuid.uuid4()

        super(Proyecto, self).save(*args, **kwargs)

    def actualizar_parte(self, contenido):
        print("todo")

    def obtener_codigo_serializado(self):
        archivo = zipfile.ZipFile(self.archivo.path, 'r')
        contenido = archivo.read("proyecto.pilas")
        return contenido.decode("utf-8")
