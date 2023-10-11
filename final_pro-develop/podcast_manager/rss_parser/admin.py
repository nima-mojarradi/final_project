from django.contrib import admin
from .models import ModelParser, Like, Comment

admin.site.register(ModelParser)
admin.site.register(Like)
admin.site.register(Comment)
