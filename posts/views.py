from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
import json
# Create your views here.
from django.conf import settings

# import viewsets
from rest_framework import viewsets
# from rest_framework.views import APIView

# import local data
from .serializers import GeeksSerializer
from .models import GeeksModel
from rest_framework.exceptions import APIException
from rest_framework import status
# create a viewset
from rest_framework.response import Response


from rest_framework.permissions import BasePermission


class sentresponse:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def response(self):
        res = dict()
        res['status'] = self.status
        res['message'] = self.message
        res['data'] = self.data
        return json.loads(json.dumps(res, indent=4))


class Needtoken(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'status': 'False', 'message': 'unauthorized', 'data': ''}
    default_code = 'not_authenticated'


class Is_User(BasePermission):
    def has_permission(self, request, view):
        try:
            request.headers["Authorization"]
        except Exception as e:
            raise Needtoken()
        if not request.headers["Authorization"]:
            raise Needtoken()
        auth_token = request.headers["Authorization"]

        if len(auth_token) > 0:
            return True
        else:
            raise Needtoken()


class GeeksViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    permission_classes = [Is_User, ]
    queryset = GeeksModel.objects.all()
    serializer_class = GeeksSerializer

    def list(self, request):
        return Response(sentresponse("true", "success", "").response())

    def create(self, request):
        seri = self.serializer_class(data=request.data)
        if seri.is_valid():
            seri.save()
            return Response(sentresponse("true", "record add", "").response())

    def retrieve(self, request, pk=None):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class GeeksViewSet1(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny, ]
    queryset = GeeksModel.objects.all()
    serializer_class = GeeksSerializer

    def list(self, request):
        return Response(sentresponse("true", "success", "").response())

    def create(self, request):
        seri = self.serializer_class(data=request.data)
        if seri.is_valid():
            seri.save()
            return Response(sentresponse("true", "record add", "").response())

    def retrieve(self, request, pk=None):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
