from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from datetime import date, datetime, timedelta
from django.contrib.auth.hashers import make_password

class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email,make_password(password), **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email,password, **extra_fields)


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
    title = models.CharField(max_length=128)
    description = models.TextField()
    code = models.CharField(max_length=64, unique=True, null=False)
    
    def __str__(self):
        return "{0} {1}".format(self.code, self.title)


class Issue(TimestampModel):
    BUG = "BUG"
    TASK = "TASK"
    STORY = "STORY"
    EPIC = "EPIC"
    TYPES = [(BUG, BUG), (TASK, TASK), (STORY, STORY), (EPIC, EPIC)]

    title = models.CharField(max_length=128)
    description = models.TextField()

    type = models.CharField(max_length=8, choices=TYPES, default=BUG, null=False)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues", null=False
    )

    def __str__(self):
        return "{0}-{1}".format(self.project.code, self.title)
