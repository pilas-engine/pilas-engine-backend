from rest_framework import viewsets
import json
from django.http import JsonResponse

from pilas.models.perfil import Perfil
from pilas.serializers.perfil import PerfilSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    resource_name = 'perfiles'

    serializer_class = PerfilSerializer
    search_fields = ['nombre']
    filter_fields = ['nombre']


def perfiles_crear_usuario(request):
    datos = json.loads(request.body)

    mi_perfil = Perfil.crear_con_usuario(datos["usuario"], datos["usuario"])
    usuario = mi_perfil.user
    usuario.set_password(datos["password"])
    usuario.email = datos["email"]
    usuario.save()

    return JsonResponse({
        "ok": True,
    }, status=200)
