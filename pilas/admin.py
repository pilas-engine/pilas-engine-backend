from django.contrib import admin
from pilas.admin_classes.proyecto import Proyecto, ProyectoAdmin
from pilas.admin_classes.perfil import Perfil, PerfilAdmin
from pilas.admin_classes.tag import Tag, TagAdmin

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Tag, TagAdmin)
