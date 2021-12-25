from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from django.conf.urls.static import static
from rest_framework.authtoken import views

from pilas.views.perfil import PerfilViewSet
from pilas.views.sesion import SesionViewSet
from pilas.views.logout import LogOutViewSet
from pilas.views.perfil import perfiles_crear_usuario
from pilas.views.perfil import perfiles_mi_perfil
from pilas.views.home import home
from pilas.views.proyecto import subir, obtener

ROOT = './static'
router = routers.DefaultRouter(trailing_slash=False)
router.register("perfiles", PerfilViewSet)


urlpatterns = [
    path('', home, name='home'),
    path('proyecto/subir', csrf_exempt(subir), name='proyecto.subir'),
    path('proyecto/obtener/<proyecto_id>', csrf_exempt(obtener), name='proyecto.obtener'),
    path('perfiles/crear-usuario', csrf_exempt(perfiles_crear_usuario), name='perfiles.crearusuario'),
    path('perfiles/mi-perfil', perfiles_mi_perfil, name='perfiles.mi_perfil'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),

    path('login/', views.obtain_auth_token),
    path('sesion/', SesionViewSet.as_view(), name='sesion'),
    path('logout/', LogOutViewSet.as_view(), name='logout'),

] + static("proyecto", document_root=ROOT)
