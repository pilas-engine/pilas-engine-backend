from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from pilas.views.proyecto import ProyectoViewSet
from pilas.views.perfil import PerfilViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("proyectos", ProyectoViewSet)
router.register("perfiles", PerfilViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
