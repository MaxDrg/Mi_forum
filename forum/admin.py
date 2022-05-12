from atexit import register
from django.contrib import admin
from .models import New, Category, Forum, Vocabulary_word
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('info',)

admin.site.register(New, PostAdmin)

admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Vocabulary_word)