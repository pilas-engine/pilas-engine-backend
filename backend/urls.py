from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from pilas.views.proyecto import ProyectoViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("proyectos", ProyectoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
