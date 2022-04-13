from . import models
from . import auth
from django.shortcuts import render

def about(request):
    return render(request, "about.html")

def aso(request):
    return render(request, "aso.html")

def curses(request):
    return render(request, "curses.html")

def forum_post(request):
    return render(request, "forum-post.html")

def forum(request):
    print(request.COOKIES.get('user_id'))
    return render(request, "forum.html")

def index(request):
    return render(request, "index.html")

def news_post(request):
    return render(request, "news-post.html")

def news(request):
    if not request.GET.get('telegr_id') == None and not request.GET.get('passwd') == None:
        user_id = request.GET.get('telegr_id')
        password = request.GET.get('passwd')

        check_user = auth.Authorization(user_id, password, True)

        response = render(request, "news.html", {
            "authorization": check_user.response
        })
        response.set_cookie( "user_id", user_id )
        response.set_cookie( "passwd", password )
        return response
    print('hello')
    return render(request, "news.html", { "data": models.User.objects.all() })

def sell(request):
    return render(request, "sell.html")

def slovar(request):
    return render(request, "slovar.html")