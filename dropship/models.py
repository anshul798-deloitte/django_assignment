from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from datetime import datetime
from .managers import MyUserManager

class Member(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
    )
    email = models.EmailField('email address', blank=False, unique=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        
    )
    is_admin=models.BooleanField(default=False)
    is_manager=models.BooleanField(default=False)
    date_joined = models.DateTimeField('date joined', default=datetime.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(TimestampModel):

    creator = models.ForeignKey(Member, related_name="manager", on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    code = models.CharField(max_length=64, unique=True, null=False)


class Label(TimestampModel):
    name = models.CharField(max_length=128)

class Issue(TimestampModel):
    BUG = "BUG"
    TASK = "TASK"
    STORY = "STORY"
    EPIC = "EPIC"
    TYPES = [(BUG, BUG), (TASK, TASK), (STORY, STORY), (EPIC, EPIC)]

    Open = "Open"
    InProgress = "InProgress"
    InReview = "InReview"
    CodeComplete = "CodeComplete"
    QATesting = "QA Testing"
    Done = "Done"

    STATUS = [(Open, Open), (InProgress, InProgress), (InReview, InReview),
              (CodeComplete, CodeComplete), (QATesting, QATesting), (Done, Done)]

    title = models.CharField(max_length=128)
    description = models.TextField()

    type = models.CharField(max_length=8, choices=TYPES, default=BUG, null=False)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues", null=False
    )
    user = models.ForeignKey(Member, related_name="reporter", on_delete=models.CASCADE)
    assignee = models.ForeignKey(Member, related_name="assignee", on_delete=models.SET_NULL, null=True)
    watchers = models.ManyToManyField(Member, related_name="watchers", blank=True)
    labels = models.ManyToManyField(Label, related_name="issues", blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default=Open, null=False)

class Comment(TimestampModel):
    user = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    issue = models.ForeignKey(Issue, related_name="comments", on_delete=models.CASCADE, default=None)
    comment = models.TextField(default="")

class Sprint(TimestampModel):

    START = "START"
    STOP = "STOP"
    TYPES = [(START, START), (STOP, STOP)]
    type = models.CharField(max_length=8, choices=TYPES, null=True)

    title = models.CharField(max_length=128)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="sprint", null=False
    )
    issues = models.ManyToManyField(Issue, related_name="sprints", blank=True)

class TimeLog(TimestampModel):
    user = models.ForeignKey(Member, on_delete=models.CASCADE,  default=None)
    estimated_time = models.CharField(max_length=10)
    logged_time = models.CharField(max_length=10)
    issue = models.ForeignKey(Issue, related_name="timelogs", on_delete=models.CASCADE, default=None)