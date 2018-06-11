from django.db import models

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200, default="")
    #pais = models.ForeignKey('Pais', related_name="proyectos", default=None, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        db_table = 'proyectos'
        verbose_name_plural = "proyectos"

    class JSONAPIMeta:
        resource_name = 'proyectos'

    def __str__(self):
        return self.nombre
