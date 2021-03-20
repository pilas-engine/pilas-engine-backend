from django.contrib import admin
from pilas.models.proyecto import Proyecto
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class ProyectoAdmin(admin.ModelAdmin):
    model = Proyecto
    list_display = ('id', 'creacion', 'imagen_tag', 'hash', 'size', 'url', 'ver_codigo')
    search_fields = ('hash', 'id')

    def url(self, obj):
        hash = str(obj.hash)
        return format_html(f"<a target='_blank' href='http://app.pilas-engine.com.ar/#/proyecto/{hash}'>ver</a>")

    def size(self, obj):
        if obj.archivo:
            s = obj.archivo.size / 1024 / 1024
            return f"{s:.2f} MB"
        else:
            return ""

    def imagen_tag(self, obj):
        if obj.imagen:
            return mark_safe(f"<img src=\"{obj.imagen.url}\" width=\"160\">")
        else:
            return ""
