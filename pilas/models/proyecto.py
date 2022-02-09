import os
import zipfile
import uuid
import shutil
from django.db import models
from django.core.files import File


class Proyecto(models.Model):
    hash = models.CharField(max_length=64, default="")
    titulo = models.CharField(max_length=256, default="Sin título")
    creacion = models.DateTimeField(auto_now_add=True, null=True)
    ver_codigo = models.BooleanField(default=True)
    archivo = models.FileField(upload_to='proyectos/', default=None, null=True)
    imagen = models.FileField(upload_to='imagenes/', default=None, null=True)
    perfil = models.ForeignKey('Perfil', related_name="proyectos", default=None, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name="proyectos")
    eliminado = models.BooleanField(default=False)

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

    def actualizar_parte(self, contenido, cantidad_de_partes, numero_de_parte):
        # Este método se ejecuta solamente cuando el proyecto
        # se envía en varias partes, porque no se pueden hacer requests muy
        # grandes a la api.

        ruta_temporal = f"/tmp/proyectos/{self.hash}"

        # Hay tres casos principales:

        # 1 - cuando llega la primer parte, se tiene que crear un directorio
        #     temporal para ir almacenando todas las partes como archivos.
        if numero_de_parte == 0:
            os.makedirs(ruta_temporal)
            self.guardar_parte(ruta_temporal, contenido, numero_de_parte)
        elif numero_de_parte == cantidad_de_partes -1:
            # 2 - Si es la última parte, tiene que guardarla, luego
            #     generar el archivo .zip y por último eliminar el directorio
            #     temporal.
            self.guardar_parte(ruta_temporal, contenido, numero_de_parte)
            self.generar_archivo_zip_desde_el_directorio(ruta_temporal)
            self.borrar_directorio_temporal(ruta_temporal)
        else:
            # 3 - Si es una parte del medio (ni la primera ni la última) entonces
            #     solo tiene que guardar la parte en el directorio temporal.
            self.guardar_parte(ruta_temporal, contenido, numero_de_parte)

    def guardar_parte(self, ruta_temporal, contenido, numero_de_parte):
        # Guarda una parte del proyecto dentro del directorio temporal
        # creado anteriormente.
        ruta = os.path.join(ruta_temporal, f"{numero_de_parte}.txt")
        archivo = open(ruta, "wt")
        archivo.write(contenido)
        archivo.close()

    def generar_archivo_zip_desde_el_directorio(self, ruta_temporal):
        listado_desordenado = os.listdir(ruta_temporal)

        def obtener_numero_de_archivo(archivo):
            primer_parte = archivo.split(".")[0]
            return int(primer_parte)

        listado  = sorted(listado_desordenado, key=obtener_numero_de_archivo)

        def obtener_contenido_del_archivo(ruta, nombre):
            ruta_completa = os.path.join(ruta, nombre)
            archivo = open(ruta_completa, "rt")
            contenido = archivo.read()
            archivo.close()
            return contenido

        contenido_de_archivos = [obtener_contenido_del_archivo(ruta_temporal, archivo) for archivo in listado]
        contenido_a_guardar = "".join(contenido_de_archivos)

        from pilas.views.proyecto import generar_archivo_desde_codigo_serializado

        ruta = generar_archivo_desde_codigo_serializado(contenido_a_guardar)
        self.archivo.save(f"{self.hash}.zip", File(open(ruta, 'rb')))
        os.remove(ruta)

    def borrar_directorio_temporal(self, ruta_temporal):
        shutil.rmtree(ruta_temporal)
        
    def obtener_codigo_serializado(self):
        archivo = zipfile.ZipFile(self.archivo.path, 'r')
        contenido = archivo.read("proyecto.pilas")
        return contenido.decode("utf-8")

    def imagen_url(self):
        if self.imagen:
            base_url = os.environ.get('BACKEND_URL')
            return base_url + self.imagen.url
        else:
            return ""

    def nombre_del_perfil(self):
        if self.perfil:
            return self.perfil.nombre
        else:
            return ""
