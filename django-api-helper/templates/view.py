from rest_framework import viewsets

from aplicacion.models.modelo import Modelo
from aplicacion.serializers.modelo import ModeloSerializer

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    resource_name = 'modelo_plural'

    serializer_class = ModeloSerializer
    search_fields = ['nombre']
    filter_fields = ['nombre']
