from django.contrib import admin

from .models import Member, Project, Issue

admin.site.register(Member)
admin.site.register(Project)
admin.site.register(Issue)
