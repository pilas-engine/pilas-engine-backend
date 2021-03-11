import os
import zipfile
import tempfile
import json
from django.shortcuts import render
from django.http import JsonResponse
import mimetypes
from django.utils._os import safe_join

from rest_framework import viewsets
from django.http import FileResponse
from django.core.files import File
from pilas.models.proyecto import Proyecto
from pilas.serializers.proyecto import ProyectoSerializer


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    resource_name = 'proyectos'

    serializer_class = ProyectoSerializer
    search_fields = ['nombre']
    filter_fields = ['nombre']

def proyecto(request, proyecto_id):
    if "-" in proyecto_id and "." not in proyecto_id:
        try:
            proyecto = Proyecto.objects.get(hash=proyecto_id)
        except Proyecto.DoesNotExist:
            return JsonResponse({
                "ok": False,
                "error": "No se encuentra este proyecto"
            }, status=404)

        context = {'proyecto_id': proyecto_id, 'proyecto': proyecto}
        return render(request, 'proyecto.html', context)
    else:
        return servir_archivo(proyecto_id)

def servir_archivo(proyecto_id):
    archivo = safe_join("static", proyecto_id)
    content_type, encoding = mimetypes.guess_type(str(archivo))
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(open(archivo, 'rb'), content_type=content_type)
    return response

def generar_archivo_desde_codigo_serializado(contenido):
    _, temp_file_path = tempfile.mkstemp()
    z = zipfile.ZipFile(temp_file_path, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('proyecto.pilas', contenido)
    z.close()

    return temp_file_path

def subir(request):
    datos = json.loads(request.body)

    if "codigo_serializado" not in datos:
        return JsonResponse({
            "ok": False,
            "error": "Faltan parámetros"
        }, status=400)

    if "hash" in datos:
        # UPDATE de parte
        raise Exception("La subida de proyectos grandes está descativada momentaneamente, por favor reintenta otro día.")
        proyecto = Proyecto.objects.get(hash=datos['hash'])
        proyecto.actualizar_parte(datos["codigo_serializado"])
        proyecto.save()
    else:
        proyecto = Proyecto.objects.create(
            ver_codigo=datos.get("ver_codigo", True)
        )

        ruta = generar_archivo_desde_codigo_serializado(datos["codigo_serializado"])
        proyecto.archivo.save(f"{proyecto.hash}.zip", File(open(ruta, 'rb')))
        os.remove(ruta)

    baseurl = os.environ.get('BACKEND_URL')
    frontendurl = os.environ.get('FRONTEND_URL')

    return JsonResponse({
        "ok": True,
        "url_test": os.path.join(baseurl, "proyecto", str(proyecto.hash)),
        "url": os.path.join(frontendurl, "#", "proyecto", str(proyecto.hash)),
        "hash": proyecto.hash,
        "error": ""
    })

def obtener(request, proyecto_id):
    proyecto = Proyecto.objects.get(hash=proyecto_id)

    return JsonResponse({
        "ok": True,
        "serializado": proyecto.obtener_codigo_serializado(),
        "ver_codigo": proyecto.ver_codigo,
        "error": ""
    })
