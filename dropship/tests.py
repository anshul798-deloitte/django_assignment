from urllib import response
from rest_framework.test import APITestCase
from django.urls import reverse
import json

class TestListCreateProjects(APITestCase):
    
    def authenticate(self):
        self.client.post(reverse("register"), {
            "username":"test",
            "email":"test@email.com",
            "password":"test123",
            "is_admin":1
        })

        response = self.client.post(reverse("login"), {
            "username":"test",
            "password":"test123"
        })
        response = json.loads(response.content)
        access = response['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    
    def test_should_create_project(self):
        self.authenticate()
        test_project = {"title":"test-project", "description":"test project", "code":"test-project123"}
        response = self.client.post(reverse("projects"), test_project)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)