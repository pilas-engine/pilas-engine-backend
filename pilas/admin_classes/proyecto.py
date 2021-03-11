import os
from django.contrib import admin
from pilas.models.proyecto import Proyecto
from django.utils.html import format_html

class ProyectoAdmin(admin.ModelAdmin):
    model = Proyecto
    list_display = ('id', 'creacion', 'hash', 'size', 'url', 'ver_codigo')
    search_fields = ('hash', 'id')

    def url(self, obj):
        baseurl = os.environ.get('BACKEND_URL')
        url = os.path.join(baseurl, "proyecto", str(obj.hash))
        return format_html("<a href='{url}'>{url}</a>", url=url)

    def size(self, obj):
        if obj.archivo:
            s = obj.archivo.size / 1024 / 1024
            return f"{s:.2f} MB"
        else:
            return ""
