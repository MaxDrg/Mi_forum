import io
from . import auth
from . import models
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

class News():
    def __init__(self, id, title, hashtags: str, date, image, info = None, pre_info = None) -> None:
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
    class Comment:
        def __init__(self, message_id, message_text: str, time: datetime, user) -> None:
            self.id = message_id
            self.message_text = message_text
            self.date = time.date()
            self.time = time.time()
            self.user = user
            self.replies = models.Comment.objects.filter(reply_to=message_id)

    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))

    if request.method == "POST":
        if request.POST['news_id'] and request.POST['message_text']:
            if check_user.response:
                if request.POST['reply_to']:
                    if request.POST['answer_to']:
                        models.Comment(
                            message_text = request.POST['message_text'],
                            reply_to = request.POST['reply_to'],
                            answer_to = request.POST['answer_to'],
                            time = datetime.now(),
                            new = models.New.objects.get(id=request.POST['news_id']),
                            user = models.User.objects.get(telegr_id=request.COOKIES.get('user_id'))
                        ).save()
                    else:
                        models.Comment(
                            message_text = request.POST['message_text'],
                            reply_to = request.POST['reply_to'],
                            time = datetime.now(),
                            new = models.New.objects.get(id=request.POST['news_id']),
                            user = models.User.objects.get(telegr_id=request.COOKIES.get('user_id'))
                        ).save()
                else:
                    models.Comment(
                        message_text = request.POST['message_text'],
                        time = datetime.now(),
                        new = models.New.objects.get(id=request.POST['news_id']),
                        user = models.User.objects.get(telegr_id=request.COOKIES.get('user_id'))
                    ).save()

            return render(request, "news-post.html", { "authorization": check_user.response, 
                "news": (lambda info: News(info.id, info.title, info.info, 
                info.pre_info, info.hashtags, info.date, info.image))
                (models.New.objects.filter(id=request.POST['news_id'])[0]) 
            })
    elif request.GET.get('news'):
        return render(request, "news-post.html", { "authorization": check_user.response, 
            "news": (lambda info: News(info.id, info.title, 
            info.hashtags, info.date, info.image, info = info.info))
            (models.New.objects.filter(id=request.GET.get('news'))[0]),
            "comments": [Comment(comment.id, comment.message_text, comment.time, comment.user) 
            for comment in models.Comment.objects.filter(new=request.GET.get('news'))]
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
            "data": [News(info.id, info.title, info.hashtags, 
            info.date, info.image, pre_info = info.pre_info)
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
        "data": [News(info.id, info.title, info.hashtags, 
        info.date, info.image, pre_info = info.pre_info)
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