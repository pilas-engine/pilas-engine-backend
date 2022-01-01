from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from pilas.models.proyecto import Proyecto


class ExplorarViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        numero_de_pagina = request.GET.get("pagina", 1)
        etiqueta = request.GET.get("etiqueta", None)
        solo_mis_juegos = request.GET.get("solo_mis_juegos", False)

        queryset = Proyecto.objects.prefetch_related("tags")

        if solo_mis_juegos:
            token = request.META.get('HTTP_AUTHORIZATION', None)

            if not token:
                return Response({"error": "Debe especificar token de usuario"}, 410)

            key = token.split(" ")[1]
            user = Token.objects.get(key=key).user
            queryset = queryset.filter(perfil=user.perfil)

        if etiqueta:
            queryset = queryset.filter(tags__nombre=etiqueta)

        paginator = Paginator(queryset, 10)
        pagina = paginator.page(numero_de_pagina)

        proyectos_serializados = [{
            "hash": proyecto.hash,
            "imagen_url": proyecto.imagen_url(),
            "titulo": proyecto.titulo,
            "creacion": proyecto.creacion,
            "perfil": proyecto.nombre_del_perfil(),
            "tags": [t.nombre for t in proyecto.tags.all()],
            } for proyecto in pagina.object_list
        ]

        return Response({
            "proyectos": proyectos_serializados,
            "total": paginator.count,
            "total_sin_paginado": Proyecto.objects.count(),
            "paginas": paginator.num_pages,
            "pagina": numero_de_pagina,
            "etiqueta": etiqueta,
            "cantidad_de_paginas": paginator.num_pages,
            "tiene_siguiente_pagina": pagina.has_next(),
            "tiene_anterior_pagina": pagina.has_previous(),
        })
