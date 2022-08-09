"""dropship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import CommentList, EmailView, IssueList, LabelList, ProjectList, LoginView, RegisterView, SprintList, TimeLogList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', RegisterView, basename='register')
router.register('projects', ProjectList, basename='projects')
router.register('issues', IssueList, basename='issues')
router.register('labels', LabelList, basename='labels')
router.register('sprints', SprintList, basename='sprints')
router.register('comments', CommentList, basename='comments')
router.register('timelogs', TimeLogList, basename='timelogs')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls, name='admin'),
    path('email/', EmailView.as_view(), name='email')
]
