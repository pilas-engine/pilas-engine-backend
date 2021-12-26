from django.contrib import admin
from pilas.models.perfil import Perfil

class PerfilAdmin(admin.ModelAdmin):
    model = Perfil
    list_display = ('id', 'nombre', 'user')
    search_fields = ('nombre', )
