from rest_framework import viewsets

from pilas.models.proyecto import Proyecto
from pilas.serializers.proyecto import ProyectoSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    resource_name = 'proyectos'

    serializer_class = ProyectoSerializer
    search_fields = ['nombre']
    filter_fields = ['nombre']
