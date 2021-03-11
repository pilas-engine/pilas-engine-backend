import os
from django.contrib import admin
from pilas.models.proyecto import Proyecto
from django.utils.html import format_html

class ProyectoAdmin(admin.ModelAdmin):
    model = Proyecto
    list_display = ('id', 'nombre', 'hash', 'url', 'ver_codigo')
    search_fields = ('nombre', )

    def change_view(self, request, object_id, extra_context=None):       
        self.exclude = ('codigo_serializado', )
        return super(ProyectoAdmin, self).change_view(request, object_id, extra_context)

    def url(self, obj):
        baseurl = os.environ.get('BACKEND_URL')
        url = os.path.join(baseurl, "proyecto", str(obj.hash))
        return format_html("<a href='{url}'>{url}</a>", url=url)
