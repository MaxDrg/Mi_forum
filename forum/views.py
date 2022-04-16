import io
from . import auth
from . import models
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

class News():
    def __init__(self, title, info, hashtags, date, image, id = None, pre_info = None) -> None:
        self.id = id
        self.title = title
        self.info = info
        self.pre_info = pre_info
        self.hashtags = hashtags.split()
        self.date = date
        self.image = image


def about(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "about.html", { "authorization": check_user.response })

def aso(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "aso.html", { "authorization": check_user.response })

def curses(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "curses.html", { "authorization": check_user.response })

def forum_post(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "forum-post.html", { "authorization": check_user.response })

def forum(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "forum.html", { "authorization": check_user.response })

def index(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "index.html", { "authorization": check_user.response })

def news_post(request):
    if request.GET.get('news'):
        check_user = auth.Authorization(
            request.COOKIES.get('user_id'), 
            request.COOKIES.get('passwd'))
        return render(request, "news-post.html", { "authorization": check_user.response, 
            "news": (lambda info: News(info.title, info.info, 
            info.hashtags, info.date, info.image))
            (models.New.objects.filter(id=request.GET.get('news'))[0]) 
        })

@csrf_exempt
def news(request):
    if request.method == "POST" and request.FILES["media_file"] and request.POST['user_id']:
        image = request.FILES["media_file"]
        image_name = f"{request.POST['user_id']}.jpg"

        fs = FileSystemStorage()

        try:
            fs.delete(image_name)
        except Exception:
            pass
        file = fs.save(image_name, io.BytesIO(image.read()))

        user = models.User.objects.get(
            telegr_id = request.POST['user_id']
        )
        user.image = fs.get_valid_name(file)
        user.save()

        return HttpResponse("OK")

    elif request.GET.get('telegr_id') and request.GET.get('passwd'):
        user_id = request.GET.get('telegr_id')
        password = request.GET.get('passwd')

        check_user = auth.Authorization(user_id, password)

        response = render(request, "news.html", {
            "authorization": check_user.response,
            "data": [News(info.title, info.info, info.hashtags,
                info.date, info.image, info.id, info.pre_info)
                for info in models.New.objects.all()]
        })

        new_password = check_user.update_pass()

        response.set_cookie( "user_id", user_id )
        response.set_cookie( "passwd", new_password )
        return response

    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))

    return render(request, "news.html", { 
        "authorization": check_user.response,
        "data": [News(info.title, info.info, info.hashtags,
            info.date, info.image, info.id, info.pre_info)
            for info in models.New.objects.all()]
    })

def sell(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "sell.html", { "authorization": check_user.response })

def slovar(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "slovar.html", { "authorization": check_user.response })