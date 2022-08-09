from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsManager, IsMember
from .models import Issue, Member, Project
from .serializers import RegisterSerializer, SignInSerializer
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import HttpResponse

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk=None):
        id = pk

        if id is not None:
            project = Project.objects.get(id=id)
            return JsonResponse(model_to_dict(project))

        projects = Project.objects.all()
        project_list = serializers.serialize('json',
                                      list(projects))
        return HttpResponse(project_list, content_type='application/json')

    def post(self, request):
        if request.data['title'] and request.data['description'] and request.data['code']:
            project = Project(creator=request.user, title=request.data['title'], description=request.data['description'], code=request.data['code'])
            project.save()
            
            return JsonResponse(model_to_dict(project))
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        id = pk
        project = Project.objects.get(id=id)

        if request.data['title'] and request.data['description'] and request.data['code']:
            project.title = request.data['title']
            project.description = request.data['description']
            project.code = request.data['code']
            project.save()
            return JsonResponse(model_to_dict(project))
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        id = pk
        project = Project.objects.get(id=id)
        project.delete()
        return Response(project)


class IssueList(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        id = pk

        if id is not None:
            issue = Issue.objects.get(id=id)
            return JsonResponse(model_to_dict(issue))

        issues = Issue.objects.all()
        issue_list = serializers.serialize('json',
                                      list(issues))
        return HttpResponse(issue_list, content_type='application/json')

    def post(self, request):
        if request.data['title'] and request.data['description'] and request.data['type'] and request.data['project']:
            project = Project.objects.get(id=request.data['project'])
            issue = Issue(reporter=request.user, title=request.data['title'], description=request.data['description'], type=request.data['type'], project=project)
            issue.save()
            
            return JsonResponse(model_to_dict(issue))
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        id = pk
        issue = Issue.objects.get(id=id)
        if request.data['title'] and request.data['description'] and request.data['type']:
            issue.title = request.data['title']
            issue.description = request.data['description']
            issue.type = request.data['type']
            issue.save()
            return JsonResponse(model_to_dict(issue))
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        id = pk
        issue = Issue.objects.get(id=id)
        user = Member.objects.get(id=request.data['assignee'])
        issue.assignee = user
        issue.save()
        return JsonResponse(model_to_dict(issue))

    def delete(self, request, pk):
        id = pk
        issue = Issue.objects.get(id=id)
        issue.delete()
        return Response(issue)