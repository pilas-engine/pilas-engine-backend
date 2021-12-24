from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import logout
import json
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action


class SesionViewSet(APIView):

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    @action(detail=False, path="logout", methods=["GET"])
    def logout(self, request, **kwargs):
        return Response("¿que?")

