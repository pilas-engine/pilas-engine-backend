from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404

from pilas.models.proyecto import Proyecto
from pilas.serializers.proyecto import ProyectoSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    resource_name = 'proyectos'

    serializer_class = ProyectoSerializer
    search_fields = ['nombre']
    filter_fields = ['nombre']

def proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    context = {'proyecto_id': proyecto_id, 'proyecto': proyecto}
    return render(request, 'proyecto.html', context)
