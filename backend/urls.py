from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from django.conf.urls.static import static
from rest_framework.authtoken import views

#from pilas.views.proyecto import ProyectoViewSet
from pilas.views.perfil import PerfilViewSet
from pilas.views.perfil import perfiles_crear_usuario
from pilas.views.home import home
from pilas.views.proyecto import proyecto, subir, obtener

ROOT = './static'
router = routers.DefaultRouter(trailing_slash=False)
#router.register("proyectos", ProyectoViewSet)
router.register("perfiles", PerfilViewSet)


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', home, name='home'),
    path('proyecto/subir', csrf_exempt(subir), name='proyecto.subir'),
    path('proyecto/obtener/<proyecto_id>', csrf_exempt(obtener), name='proyecto.obtener'),
    path('proyecto/<proyecto_id>', proyecto, name='proyecto.ver'),
    path('perfiles/crear-usuario', csrf_exempt(perfiles_crear_usuario), name='perfiles.crearusuario'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static("proyecto", document_root=ROOT)
