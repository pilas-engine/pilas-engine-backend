from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

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

    usuarios_con_ese_nombre = User.objects.filter(username=datos["usuario"])
    existe = usuarios_con_ese_nombre.count() > 0

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

    token, created = Token.objects.get_or_create(user=usuario)

    return JsonResponse({
        "ok": True,
        "token": token.key,
    }, status=200)


@api_view(('GET',))
@renderer_classes((JSONRenderer, ))
def perfiles_mi_perfil(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)

    if token:
        key = token.split(" ")[1]
        user = Token.objects.get(key=key).user

        return Response({
            "nombre": user.perfil.nombre
        })
    else:
        return Response({
            "error": "Debe especificar el token de acceso"
        }, 401)



@api_view(('GET',))
@renderer_classes((JSONRenderer, ))
def perfiles_mis_juegos(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    from pilas.views.explorar import obtener_proyectos_serializados

    if token:
        key = token.split(" ")[1]
        user = Token.objects.get(key=key).user

        numero_de_pagina = request.GET.get("pagina", 1)
        etiqueta = request.GET.get("etiqueta", None)

        queryset = user.perfil.proyectos.prefetch_related("tags").all()

        data = obtener_proyectos_serializados(queryset, etiqueta, numero_de_pagina)

        return Response(data)
    else:
        return Response({
            "error": "Debe especificar el token de acceso"
        }, 401)


