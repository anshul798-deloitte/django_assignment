from django.contrib.auth import authenticate
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin, IsManager, IsAdminOrOwner
from .models import Issue, Member, Project, Label, Sprint, Comment, TimeLog
from .serializers import CommentSerializer, EmailSerializer, IssueSerializer, LabelSerializer, RegisterSerializer, SignInSerializer, ProjectSerializer, SprintSerializer, TimeLogSerializer

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class RegisterView(ModelViewSet):
    permission_classes = []
    serializer_class = RegisterSerializer
    queryset = Member.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class LoginView(APIView):
    permission_classes = []

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


class ProjectList(ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

class IssueList(ModelViewSet):
    permission_classes = [IsAdminOrOwner]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    filterset_fields = ['title','type','project','user','assignee','watchers','status', 'labels']

class SprintList(ModelViewSet):
    permission_classes = [IsManager|IsAdmin]
    serializer_class = SprintSerializer
    queryset = Sprint.objects.all()
    filterset_fields = ['title','start_date','end_date','type','project']

class LabelList(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LabelSerializer
    queryset = Label.objects.all()

class CommentList(ModelViewSet):
    permission_classes = [IsAdminOrOwner]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filterset_fields = ['user','issue']

class TimeLogList(ModelViewSet):
    permission_classes = [IsAdminOrOwner]
    serializer_class = TimeLogSerializer
    queryset = TimeLog.objects.all()
    filterset_fields = ['user','issue']

class EmailView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():

            issue = Issue.objects.get(id=serializer.data['issue'])
            recipients = issue.watchers.all()
            for recipient in recipients:

                message = Mail(
                    from_email='anshulbhardwaj987@gmail.com',
                    to_emails=recipient.email,
                    subject='Sending with Twilio SendGrid is Fun',
                    html_content= serializer.data['message'])

                sg = SendGridAPIClient('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')
                response = sg.send(message)
                print(response)

            return Response("Mail Sent!")

        else:
            return Response("Mail Not Sent!")

        

    