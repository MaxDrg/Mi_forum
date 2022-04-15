import io
from . import auth
from . import models
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

def about(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "about.html", { "authorization": check_user.response })

def aso(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "aso.html", { "authorization": check_user.response })

def curses(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "curses.html", { "authorization": check_user.response })

def forum_post(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "forum-post.html", { "authorization": check_user.response })

def forum(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "forum.html", { "authorization": check_user.response })

def index(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "index.html", { "authorization": check_user.response })

def news_post(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "news-post.html", { "authorization": check_user.response })

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
            "authorization": check_user.response
        })

        new_password = check_user.update_pass()
        response.set_cookie( "user_id", user_id )
        response.set_cookie( "passwd", new_password )
        return response

    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "news.html", { "authorization": check_user.response })

def sell(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "sell.html", { "authorization": check_user.response })

def slovar(request):
    check_user = auth.Authorization(
        request.COOKIES.get('telegr_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "slovar.html", { "authorization": check_user.response })