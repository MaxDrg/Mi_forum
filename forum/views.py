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
    return render(request, "forum.html")

def index(request):
    return render(request, "index.html")

def news_post(request):
    return render(request, "news-post.html")

def news(request):
    return render(request, "news.html")

def sell(request):
    return render(request, "sell.html")

def slovar(request):
    return render(request, "slovar.html")