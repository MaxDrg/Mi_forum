import turtle
from . import models
from . import auth
from PIL import Image
import io
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def news(request):
    if request.method == "POST" and request.FILES["media_file"] and request.POST['user_id']:
        image = request.FILES["media_file"]
        image_name = f"{request.POST['user_id']}.jpg"

        try:
            fs.delete(image_name)
        except:
            pass

        image_file = Image.open(io.BytesIO(image))
        fs = FileSystemStorage()
        fs.save(image_name, image_file)
        
        user = models.User.objects.get(
            telegr_id = request.POST['user_id']
        )
        print(user)
        user.image = image_name
        user.save()

        print("i get it")
        return render(request, "index.html")

    elif not request.GET.get('telegr_id') and not request.GET.get('passwd'):
        user_id = request.GET.get('telegr_id')
        password = request.GET.get('passwd')

        check_user = auth.Authorization(user_id, password, True)

        response = render(request, "news.html", {
            "authorization": check_user.response
        })
        print('world')
        response.set_cookie( "user_id", user_id )
        response.set_cookie( "passwd", password )
        return response
    print('hello')
    return render(request, "news.html", { "data": models.User.objects.all() })

def sell(request):
    return render(request, "sell.html")

def slovar(request):
    return render(request, "slovar.html")