from django.contrib import admin
from pilas.models.proyecto import Proyecto

class ProyectoAdmin(admin.ModelAdmin):
    model = Proyecto
    list_display = ('id', 'nombre')
    search_fields = ('nombre', )
