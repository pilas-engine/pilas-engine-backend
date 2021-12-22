from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from django.conf.urls.static import static
from rest_framework.authtoken import views

#from pilas.views.proyecto import ProyectoViewSet
from pilas.views.perfil import PerfilViewSet
from pilas.views.sesion import SesionViewSet
from pilas.views.perfil import perfiles_crear_usuario
from pilas.views.perfil import perfiles_obtener_perfil_desde_token
from pilas.views.perfil import perfiles_logout
from pilas.views.home import home
from pilas.views.proyecto import proyecto, subir, obtener

ROOT = './static'
router = routers.DefaultRouter(trailing_slash=False)
router.register("perfiles", PerfilViewSet)


urlpatterns = [
    path('', home, name='home'),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-token-logout/', perfiles_logout),
    path('proyecto/subir', csrf_exempt(subir), name='proyecto.subir'),
    path('proyecto/obtener/<proyecto_id>', csrf_exempt(obtener), name='proyecto.obtener'),
    path('proyecto/<proyecto_id>', proyecto, name='proyecto.ver'),
    path('perfiles/crear-usuario', csrf_exempt(perfiles_crear_usuario), name='perfiles.crearusuario'),
    path('perfiles/obtener-perfil-desde-token/<token>', perfiles_obtener_perfil_desde_token, name='perfiles.obtener_perfil_desde_token'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('sesion/', SesionViewSet.as_view(), name='sesion'),
] + static("proyecto", document_root=ROOT)
