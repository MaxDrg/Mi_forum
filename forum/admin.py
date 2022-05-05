from atexit import register
from django.contrib import admin
from .models import New, Category, Forum, Vocabulary_word

admin.site.register(New)
admin.site.register(Category)
admin.site.register(Forum)
admin.site,register(Vocabulary_word)
