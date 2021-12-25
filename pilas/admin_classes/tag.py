from django.contrib import admin
from pilas.models.tag import Tag

class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('id', 'nombre', 'cantidad_de_proyectos')
    search_fields = ('nombre', 'id')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('proyectos')

    def cantidad_de_proyectos(self, instance):
        return instance.proyectos.count()
