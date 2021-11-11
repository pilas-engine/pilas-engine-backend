from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
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

    existe = User.objects.filter(username=datos["usuario"]).count() > 0

    if existe:
        return JsonResponse({
            "ok": False,
            "error": "El usuario ya existe",
        }, status=500)

    mi_perfil = Perfil.crear_con_usuario(datos["usuario"], datos["usuario"])
    usuario = mi_perfil.user
    usuario.set_password(datos["password"])
    usuario.email = datos["email"]
    usuario.save()

    return JsonResponse({
        "ok": True,
    }, status=200)


def perfiles_obtener_perfil_desde_token(request, token):
    user = Token.objects.get(key=token).user

    return JsonResponse({
        "nombre": user.perfil.nombre
    })
