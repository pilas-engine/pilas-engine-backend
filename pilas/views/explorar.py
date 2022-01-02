from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
import itertools

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
        mostrar_recientes_agrupados = request.GET.get(
            "mostrar_recientes_agrupados", False)

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

            if mostrar_recientes_agrupados:
                proyectos_agrupados = self.serializar_proyectos_agrupados_por_usuario(queryset)

                return Response({
                    "proyectos_agrupados": proyectos_agrupados,
                    "total": len(queryset),
                    "total_sin_paginado": len(queryset),
                    "paginas": 1,
                    "pagina": 1,
                    "etiqueta": etiqueta,
                    "cantidad_de_paginas": 1,
                    "tiene_siguiente_pagina": False,
                    "tiene_anterior_pagina": False,
                })

        return Response(obtener_proyectos_serializados(queryset, etiqueta, numero_de_pagina))

    def serializar_proyectos_agrupados_por_usuario(self, proyectos):
        resultado = itertools.groupby(proyectos, lambda x: x.perfil)

        def obtener_etiqueta(perfil):
            if perfil:
                return perfil.nombre
            else:
                return "Sin autenticar"

        return [
                {
                    "perfil": obtener_etiqueta(usuario),
                    "proyectos": list([serializar_un_proyecto(p) for p in proyectos_del_usuario]),
                } for usuario, proyectos_del_usuario in resultado
        ]

def serializar_un_proyecto(proyecto):
    return {
        "hash": proyecto.hash,
        "imagen_url": proyecto.imagen_url(),
        "titulo": proyecto.titulo,
        "creacion": proyecto.creacion,
        "perfil": proyecto.nombre_del_perfil(),
        "tags": [t.nombre for t in proyecto.tags.all()],
    }

def obtener_proyectos_serializados(queryset, etiqueta, numero_de_pagina):
    paginator = Paginator(queryset, 10)
    pagina = paginator.page(numero_de_pagina)

    proyectos_serializados = [
        serializar_un_proyecto(proyecto)
        for proyecto in pagina.object_list
    ]

    return {
        "proyectos": proyectos_serializados,
        "total": paginator.count,
        "total_sin_paginado": Proyecto.objects.count(),
        "paginas": paginator.num_pages,
        "pagina": numero_de_pagina,
        "etiqueta": etiqueta,
        "cantidad_de_paginas": paginator.num_pages,
        "tiene_siguiente_pagina": pagina.has_next(),
        "tiene_anterior_pagina": pagina.has_previous(),
    }
