from django.contrib import admin
from pilas.models.proyecto import Proyecto
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class ProyectoAdmin(admin.ModelAdmin):
    model = Proyecto
    list_display = (
            'id', 
            'titulo', 
            'imagen_tag', 
            'lista_de_tags', 
            'perfil',
            'size', 
            'url', 
            'ver_codigo',
            'creacion',
    )
    search_fields = (
            'hash', 
            'id',
    )

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

    def lista_de_tags(self, obj):
        return ", ".join([t.nombre for t in obj.tags.all()])

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('tags')
