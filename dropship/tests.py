import email
from rest_framework.test import APITestCase
from django.urls import reverse
import json
from .models import Member


class TestProjects(APITestCase):
    
    def authenticate(self):
        response = self.client.post(reverse("register-list"), {
            "username":"test",
            "email":"test@email.com",
            "password":"test123",
            "is_admin":1
        })
        self.userId = json.loads(response.content)["id"]
        response = self.client.post(reverse("login"), {
            "username":"test",
            "password":"test123"
        })
        response = json.loads(response.content)
        access = response['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def setUp(self):
        self.authenticate()

    def test_should_create_project(self):
        test_project = {"title":"test-project", "description":"test project", "code":"test-project123", "creator":self.userId}
        response = self.client.post(reverse("projects-list"), test_project)
        self.assertEqual(response.status_code, 201)
    
    def test_should_delete_project(self):
        test_project = {"title":"test-project", "description":"test project", "code":"test-project123", "creator":self.userId}
        self.client.post(reverse("projects-list"), test_project)
        response = self.client.delete(reverse("projects-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 204)

class TestIssues(APITestCase):

    def authenticate(self):
        response = self.client.post(reverse("register-list"), {
            "username":"test",
            "email":"test@email.com",
            "password":"test123",
            "is_admin":1
        })
        self.userId = json.loads(response.content)["id"]
        response = self.client.post(reverse("login"), {
            "username":"test",
            "password":"test123"
        })
        response = json.loads(response.content)
        access = response['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def setUp(self):
        self.authenticate()
        test_project = {"title":"test-project", "description":"test project", "code":"test-project123", "creator":self.userId}
        self.client.post(reverse("projects-list"), test_project)
    
    def test_should_create_issue(self):
        test_issue = {"title":"test", "description":"test", "type":"BUG", "project":"1", "user":self.userId,"status":"Open"}
        response = self.client.post(reverse("issues-list"), test_issue)
        self.assertEqual(response.status_code, 201)
    
    def test_should_delete_issue(self):
        test_issue = {"title":"test", "description":"test", "type":"BUG", "project":"1", "user":self.userId,"status":"Open"}
        self.client.post(reverse("issues-list"), test_issue)
        response = self.client.delete(reverse("issues-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 204)

class TestLabels(APITestCase):

    def authenticate(self):
        response = self.client.post(reverse("register-list"), {
            "username":"test",
            "email":"test@email.com",
            "password":"test123",
            "is_admin":1
        })
        self.userId = json.loads(response.content)["id"]
        response = self.client.post(reverse("login"), {
            "username":"test",
            "password":"test123"
        })
        response = json.loads(response.content)
        access = response['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def setUp(self):
        self.authenticate()
    
    def test_should_create_labels(self):
        test_lables = {"name":"test label"}
        response = self.client.post(reverse("labels-list"), test_lables)
        self.assertEqual(response.status_code, 201)
    
    def test_should_delete_labels(self):
        test_lables = {"name":"test label"}
        self.client.post(reverse("labels-list"), test_lables)
        response = self.client.delete(reverse("labels-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 204)

class TestSprint(APITestCase):
    def authenticate(self):
        response = self.client.post(reverse("register-list"), {
            "username":"test",
            "email":"test@email.com",
            "password":"test123",
            "is_admin":1
        })
        self.userId = json.loads(response.content)["id"]
        response = self.client.post(reverse("login"), {
            "username":"test",
            "password":"test123"
        })
        response = json.loads(response.content)
        access = response['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def setUp(self):
        self.authenticate()
        test_project = {"title":"test-project", "description":"test project", "code":"test-project123", "creator":self.userId}
        self.client.post(reverse("projects-list"), test_project)
        test_issue = {"title":"test", "description":"test", "type":"BUG", "project":"1", "user":self.userId,"status":"Open", "watchers":[1]}
        self.client.post(reverse("issues-list"), test_issue)
    
    def test_should_create_sprint(self):
        test_sprint = {"type":"START","title":"test Sprint", "description":"test", "start_date":"2022-08-01", "end_date":"2022-08-07","project":1,"issues":[1]}
        response = self.client.post(reverse("sprints-list"), test_sprint)
        self.assertEqual(response.status_code, 201)
    
    def test_should_delete_sprint(self):
        test_sprint = {"type":"START","title":"test Sprint", "description":"test", "start_date":"2022-08-01", "end_date":"2022-08-07","project":1,"issues":[1]}
        self.client.post(reverse("sprints-list"), test_sprint)

        response = self.client.delete(reverse("sprints-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 204)

class TestComment(APITestCase):
    def authenticate(self):
        response = self.client.post(reverse("register-list"), {
            "username":"test",
            "email":"test@email.com",
            "password":"test123",
            "is_admin":1
        })
        self.userId = json.loads(response.content)["id"]
        response = self.client.post(reverse("login"), {
            "username":"test",
            "password":"test123"
        })
        response = json.loads(response.content)
        access = response['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def setUp(self):
        self.authenticate()
        test_project = {"title":"test-project", "description":"test project", "code":"test-project123", "creator":self.userId}
        self.client.post(reverse("projects-list"), test_project)
        test_issue = {"title":"test", "description":"test", "type":"BUG", "project":"1", "user":self.userId,"status":"Open", "watchers":[1]}
        self.client.post(reverse("issues-list"), test_issue)
    
    def test_should_create_comment(self):
        test_comment = {"issue":1, "user":1, "comment":"Test Comment"}
        response = self.client.post(reverse("comments-list"), test_comment)
        self.assertEqual(response.status_code, 201)

class TestEmail(APITestCase):
    def authenticate(self):
        response = self.client.post(reverse("register-list"), {
            "username":"test",
            "email":"test@email.com",
            "password":"test123",
            "is_admin":1
        })
        self.userId = json.loads(response.content)["id"]
        response = self.client.post(reverse("login"), {
            "username":"test",
            "password":"test123"
        })
        response = json.loads(response.content)
        access = response['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def setUp(self):
        self.authenticate()
        test_project = {"title":"test-project", "description":"test project", "code":"test-project123", "creator":self.userId}
        self.client.post(reverse("projects-list"), test_project)
        test_issue = {"title":"test", "description":"test", "type":"BUG", "project":"1", "user":self.userId,"status":"Open", "watchers":[1]}
        self.client.post(reverse("issues-list"), test_issue)
        Member.objects.create(username="test-username", password="123456", email="test@esmail.com")
    
    def test_should_send_email(self):
        test_email = {"message":"test email sent", "issue":1}
        response = self.client.post(reverse("email"), test_email)
        self.assertEqual(response.status_code, 200)