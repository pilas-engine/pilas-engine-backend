from rest_framework import viewsets

from pilas.models.perfil import Perfil
from pilas.serializers.perfil import PerfilSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    resource_name = 'perfiles'

    serializer_class = PerfilSerializer
    search_fields = ['nombre']
    filter_fields = ['nombre']
