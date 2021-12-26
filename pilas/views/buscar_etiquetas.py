from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout
from pilas.models.tag import Tag


class BuscarEtiquetasViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        query = request.GET.get("query", "")

        data = Tag.objects.filter(nombre__icontains=query).values_list("nombre", flat=True)[:10]

        return Response(data, status=200)
