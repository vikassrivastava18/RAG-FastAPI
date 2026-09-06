from django.contrib import admin

# Register your models here.
from .models import Course, Topic, SubTopic, CodeSnippet

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(CodeSnippet)