from django.contrib import admin
from .models import User, New, Comment

admin.site.register(User)
admin.site.register(New)
admin.site.register(Comment)