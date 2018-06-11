from django.contrib import admin
from aplicacion.models.modelo import Modelo

class ModeloAdmin(admin.ModelAdmin):
    model = Modelo
    list_display = ('id', 'nombre')
    search_fields = ('nombre', )
