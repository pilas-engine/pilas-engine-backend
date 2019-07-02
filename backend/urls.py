from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from pilas.views.proyecto import ProyectoViewSet
from pilas.views.perfil import PerfilViewSet
from pilas.views.home import home
from pilas.views.proyecto import proyecto

router = routers.DefaultRouter(trailing_slash=False)
router.register("proyectos", ProyectoViewSet)
router.register("perfiles", PerfilViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('proyecto/<int:proyecto_id>/', proyecto, name='proyecto'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
