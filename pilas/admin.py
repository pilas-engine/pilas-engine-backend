from django.contrib import admin
from pilas.admin_classes.proyecto import Proyecto, ProyectoAdmin

admin.site.register(Proyecto, ProyectoAdmin)
