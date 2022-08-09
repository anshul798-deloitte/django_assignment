from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin, IsManager, IsMember
from .models import Project
from .serializers import ProjectSerializer
from .serializers import SignInSerializer
from django.contrib.auth import authenticate
from django.http import JsonResponse

class LoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        received_json_data=request.data
        serializer = SignInSerializer(data=received_json_data)
        if serializer.is_valid():
            userauth = authenticate(
                request, 
                username=received_json_data['username'], 
                password=received_json_data['password'])
            if userauth is not None:
                refresh = RefreshToken.for_user(userauth)
                return JsonResponse({
                    'status':200,
                    'data':{
                    'username':userauth.get_username(),
                    'is_admin':userauth.is_admin,
                    'is_manager':userauth.is_manager,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                }, status=200)
            else:
                return JsonResponse({
                    'message': 'invalid username or password',
                }, status=403)
        else:
            return JsonResponse({'message':serializer.errors}, status=400)

class ProjectList(APIView):

    def get(self, request, pk=None):
        id = pk

        if id is not None:
            project = Project.objects.get(id=id)
            serialize = ProjectSerializer(project)
            return Response(serialize.data)

        projects = Project.objects.all()
        serialize = ProjectSerializer(projects, many=True)
        return Response(serialize.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        id = pk
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(instance=project ,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        id = pk
        project = Project.objects.get(id=id)
        project.delete()
        return Response(project)