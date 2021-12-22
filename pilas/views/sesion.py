from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import logout
import json
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

class SesionViewSet(APIView):

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    @classmethod
    def get_extra_actions(cls):
        return []

