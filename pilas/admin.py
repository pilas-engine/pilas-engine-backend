from django.contrib import admin
from pilas.admin_classes.proyecto import Proyecto, ProyectoAdmin
from pilas.admin_classes.perfil import Perfil, PerfilAdmin

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Perfil, PerfilAdmin)
