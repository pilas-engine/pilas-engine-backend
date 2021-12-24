from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout


class LogOutViewSet(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        data = {"success": "Successfully logged out."}
        return Response(data, status=200)
