import os
from django.contrib import admin
from pilas.models.proyecto import Proyecto
from django.utils.html import format_html

class ProyectoAdmin(admin.ModelAdmin):
    model = Proyecto
    list_display = ('id', 'creacion', 'hash', 'size', 'url', 'ver_codigo')
    search_fields = ('hash', 'id')

    def url(self, obj):
        hash = str(obj.hash)
        return format_html(f"<a target='_blank' href='http://localhost:4200/#/proyecto/{hash}'>ver</a>")

    def size(self, obj):
        if obj.archivo:
            s = obj.archivo.size / 1024 / 1024
            return f"{s:.2f} MB"
        else:
            return ""
