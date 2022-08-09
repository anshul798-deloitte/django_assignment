from django.contrib import admin

from .models import Member, Project, Issue, Label, Comment, Sprint, TimeLog

admin.site.register(Member)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Label)
admin.site.register(Comment)
admin.site.register(Sprint)
admin.site.register(TimeLog)