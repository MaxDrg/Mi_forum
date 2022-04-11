from django.urls import path
from . import views
# import hashlib

urlpatterns = [
    path('about', views.about, name='about'),
    path('aso', views.aso, name='aso'),
    path('curses', views.curses, name='curses'),
    path('forum-post', views.forum_post, name='forum-post'),
    path('forum', views.forum, name='forum'),
    path('index', views.index, name='index'),
    path('news-post', views.news_post, name='news-post'),
    path('news', views.news, name='news'),
    path('sell', views.sell, name='sell'),
    path('slovar', views.slovar, name='slovar'),
    #path(hashlib.sha256('buckets'.encode('utf8')).hexdigest(), views.buckets, name='buckets')
]