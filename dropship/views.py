from multiprocessing import ProcessError
from xmlrpc.client import ResponseError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Project
from .serializers import ProjectSerializer

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
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        id = pk
        project = Project.objects.get(id=id)
        project.delete()
        return Response(project)