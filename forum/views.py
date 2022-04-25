import io
import telegram
from . import auth
from . import models
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

class Receiver:
    def __init__(self, first_name, user_name) -> None:
        self.first_name = first_name
        self.user_name = user_name

class Message:
    def __init__(self, message_id: int, message_text: str, 
    time: datetime, user: models.User, image: str) -> None:
        self.id = message_id
        self.message_text = message_text
        self.date = time.date()
        self.time = time.strftime('%H:%M')
        self.user = user
        self.image = image
        self.replies = [Reply(reply.id, reply.message_text, reply.time, 
        reply.user, reply.image, reply.is_answer, reply.receiver) 
        for reply in models.Message.objects.filter(reply_to=self.id)]
            
class Reply(Message):
    def __init__(self, message_id: int, message_text: str, time: datetime, 
    user: models.User, image: str, is_answer: bool, receiver: int) -> None:
        super().__init__(message_id, message_text, time, user, image)
        self.__is_answer = is_answer
        self.__receiver = receiver
        self.receiver = None
        if self.__is_answer:
            user = models.User.objects.filter(id=self.__receiver).values('first_name', 'user_name')[0]
            if user['user_name'] == None:
                self.receiver = Receiver(user['first_name'], False)
            else:
                self.receiver = Receiver(user['first_name'], user['user_name'])

class Topic:
    def __init__(self, id: int, name: str, description: str) -> None:
        self.id = id
        self.name = name
        self.description = description

class News():
    def __init__(self, id: int, title: str, hashtags: str, date: datetime, 
    image: str, info: str = None, pre_info: str = None) -> None:
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
    return render(request, "about.html", { "authorization": check_user.response,
    "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
    if response else False)(check_user.response) })

def aso(request):
    alert = False
    if request.method == "POST":
        if request.POST['name'] and request.POST['telegram']:
            post_on_telegram(
                name = request.POST['name'],
                link =  (lambda link: link if link else "")(request.POST['link']),
                telegram_account = request.POST['telegram']
            )
            alert = True
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "aso.html", { "authorization": check_user.response,
    "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
    if response else False)(check_user.response), 'alert': alert})

def curses(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "curses.html", { "authorization": check_user.response,
    "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
    if response else False)(check_user.response) })

def forum_post(request):

    class Forum_post:
        def __init__(self, forum: models.Forum) -> None:
            self.category_id = forum.category.id
            self.category_name = forum.category.name
            self.forum_id = forum.id
            self.forum_name = forum.name

    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))

    if request.method == "POST":
        if request.POST['forum_id'] and request.POST['message_text'] and check_user.response:
            if request.POST['reply_to'] and request.POST['receiver']:
                new_message = models.Message(
                    message_text = request.POST['message_text'],
                    reply_to = request.POST['reply_to'],
                    receiver = request.POST['receiver'],
                    time = datetime.now(),
                    forum = models.Forum.objects.get(id=request.POST['forum_id']),
                    user = models.User.objects.get(telegr_id=request.COOKIES.get('user_id')),
                    is_answer = (lambda response: True if response else False)(request.POST['is_answer'])
                )
            else:
                new_message = models.Message(
                    message_text = request.POST['message_text'],
                    time = datetime.now(),
                    forum = models.Forum.objects.get(id=request.POST['forum_id']),
                    user = models.User.objects.get(telegr_id=request.COOKIES.get('user_id')),
                    is_answer = False
                )
            image = None
            if request.FILES.get('image'):
                fs = FileSystemStorage()
                file = fs.save(new_message.id, request.FILES['image'])
                image = fs.get_valid_name(file)
            new_message.image = image
            new_message.save()

            return render(request, "forum-post.html", { "authorization": check_user.response,
                "forum": Forum_post(models.Forum.objects.filter(id=request.POST['forum_id'])[0]),
                "messages": [Message(message.id, message.message_text, 
                message.time, message.user, message.image)
                for message in models.Message.objects.filter(
                    forum=request.POST['forum_id'], 
                    reply_to=None)],
                "notifications": (lambda response: get_notification(
                    request.COOKIES.get('user_id')) 
                if response else False)(check_user.response)
            })
    elif request.GET.get('forum'):
        for i in[print(message.message_text)
            for message in models.Message.objects.filter(
                forum=request.GET.get('forum'), 
                reply_to=None)]:
            print(i)
        
        return render(request, "forum-post.html", { "authorization": check_user.response, 
            "forum": Forum_post(models.Forum.objects.filter(id=request.GET.get('forum'))[0]),
            "messages": [Message(message.id, message.message_text, 
            message.time, message.user, message.image)
            for message in models.Message.objects.filter(
                forum=request.GET.get('forum'), 
                reply_to=None)],
            "notifications": (lambda response: get_notification(
                request.COOKIES.get('user_id')) 
            if response else False)(check_user.response)
        })

def forum(request):
    class Last_message_user():
        def __init__(self, time: datetime, first_name: str, user_name: str, image: str) -> None:
            self.date = time.date()
            self.time = time.strftime('%H:%M')
            self.first_name = first_name
            self.user_name = user_name
            self.image = image

    class Forum(Topic):
        def __init__(self, id: int, name: str, description: str, private: bool) -> None:
            super().__init__(id, name, description)
            self.messages_count = models.Message.objects.filter(forum=id, reply_to=None).count()
            self.private = private
            self.last_message_user = False
            message = models.Message.objects.filter(forum=id).last()
            if message:
                user = message.user
                self.last_message_user = Last_message_user(message.time, user.first_name,
                user.user_name, user.image)

    if request.GET.get('category'):
        check_user = auth.Authorization(
            request.COOKIES.get('user_id'), 
            request.COOKIES.get('passwd'))
        sub = False
        if check_user.response:
            sub = models.User.objects.filter(telegr_id=request.COOKIES.get('user_id'))
        return render(request, "forum.html", { "authorization": check_user.response,
        'subscription': (lambda user: True if user else False)(sub),
        "category": models.Category.objects.filter(id=request.GET.get('category')).values('name')[0],
        "forums": [Forum(forum.id, forum.name, forum.description, forum.private) 
        for forum in models.Forum.objects.filter(category=request.GET.get('category'))],
        "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
        if response else False)(check_user.response) })

def index(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "index.html", { "authorization": check_user.response,
    "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
    if response else False)(check_user.response) })

def news_post(request):

    class Comment(Message):
        def __init__(self, message_id, message_text: str, time: datetime, user, image = None) -> None:
            super().__init__(message_id, message_text, time, user, image)
            self.replies = [Reply(reply.id, reply.message_text, 
            reply.time, reply.user, None, reply.is_answer, reply.receiver) 
            for reply in models.Comment.objects.filter(reply_to=self.id)]

    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))

    if request.method == "POST":
        if request.POST['news_id'] and request.POST['message_text'] and check_user.response:
            if request.POST['reply_to'] and request.POST['receiver']:
                models.Comment(
                    message_text = request.POST['message_text'],
                    reply_to = request.POST['reply_to'],
                    receiver = request.POST['receiver'],
                    time = datetime.now(),
                    new = models.New.objects.get(id=request.POST['news_id']),
                    user = models.User.objects.get(telegr_id=request.COOKIES.get('user_id')),
                    is_answer = (lambda response: True if response else False)(request.POST['is_answer'])
                ).save()
            else:
                models.Comment(
                    message_text = request.POST['message_text'],
                    time = datetime.now(),
                    new = models.New.objects.get(id=request.POST['news_id']),
                    user = models.User.objects.get(telegr_id=request.COOKIES.get('user_id')),
                    is_answer = False
                ).save()

            return render(request, "news-post.html", { "authorization": check_user.response, 
                "news": (lambda info: News(info.id, info.title, 
                info.hashtags, info.date, info.image, info = info.info))
                (models.New.objects.filter(id=request.POST['news_id'])[0]),
                "comments": [Comment(comment.id, comment.message_text, comment.time, comment.user) 
                for comment in models.Comment.objects.filter(new=request.POST['news_id'], reply_to=None)],
                "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
                if response else False)(check_user.response)
            })
    elif request.GET.get('news'):
        return render(request, "news-post.html", { "authorization": check_user.response, 
            "news": (lambda info: News(info.id, info.title, 
            info.hashtags, info.date, info.image, info = info.info))
            (models.New.objects.filter(id=request.GET.get('news'))[0]),
            "comments": [Comment(comment.id, comment.message_text, comment.time, comment.user) 
            for comment in models.Comment.objects.filter(new=request.GET.get('news'), reply_to=None)],
            "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
            if response else False)(check_user.response)
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
            for info in models.New.objects.all()],
            "notifications": (lambda response: get_notification(request.GET.get('telegr_id')) 
            if response else False)(check_user.response)
        })

        if check_user.response:
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
        for info in models.New.objects.all()],
        "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
        if response else False)(check_user.response)
    })

def sell(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "sell.html", { "authorization": check_user.response, 
    "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
    if response else False)(check_user.response)})

def slovar(request):
    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "slovar.html", { "authorization": check_user.response,
    "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
    if response else False)(check_user.response)})

def categories(request):

    class Last_message_forum:
        def __init__(self, message: models.Message) -> None:
            self.id = message.forum.id
            self.name = message.forum.name
            self.time = message.time.strftime('%H:%M')
            self.date = message.time.date()

    class Category(Topic):
        def __init__(self, id: int, name: str, description: str) -> None:
            super().__init__(id, name, description)
            self.forums_count = models.Forum.objects.filter(category=id).count()
            self.last_message_forum = False
            messages = []
            for forum in models.Forum.objects.filter(category=id):
                last_message = models.Message.objects.filter(forum=forum.id).last()
                if last_message:
                    messages.append(last_message)
            if messages:
                time = messages[0].time
                self.last_message_forum = Last_message_forum(messages[0])
                for message in messages:
                    if time < message.time:
                        time = message.time
                        self.last_message_forum = Last_message_forum(message)

    check_user = auth.Authorization(
        request.COOKIES.get('user_id'), 
        request.COOKIES.get('passwd'))
    return render(request, "categories.html", { "authorization": check_user.response, 
    "categories": [Category(category.id, category.name, category.description) 
    for category in models.Category.objects.all()],
    "notifications": (lambda response: get_notification(request.COOKIES.get('user_id')) 
    if response else False)(check_user.response)})

def post_on_telegram(name: str, link: str, telegram_account: str):
    message_txt = f'Заявка "ASO Оптимизация"\nИмя: {name}' \
    f'\nСсылка на проект: {link}\nTelegram для связи: {telegram_account}'
    
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id=telegram_settings['chat_id'],
                     text=message_txt, parse_mode=telegram.ParseMode.HTML)

def get_notification(telegr_id: int):
    class Notice:
        def __init__(self, id: int, name: str, time: datetime, type: str) -> None:
            self.id = id
            self.name = name
            self.time = time.strftime('%H:%M')
            self.type = type
    
    class Notifications:
        def __init__(self, today_notice, yesterday_notice) -> None:
            self.today = today_notice
            self.yesterday = yesterday_notice

    def unique(input_list: list):
        unique_messages = []
        unique_comments = []
        unique_list = []
        for data in input_list:
            if data.type == 'message':
                if data.id not in unique_messages:
                    unique_messages.append(data.id)
                    unique_list.append(data)
            else:
                if data.id not in unique_comments:
                    unique_comments.append(data.id)
                    unique_list.append(data)
        return unique_list

    user_id = models.User.objects.filter(telegr_id=telegr_id)[0].id
    topics_today = []
    topics_yesterday = []
    
    day_now = datetime.now()
    day_yesterday = (datetime.now() - timedelta(days=1))

    messages_today = models.Message.objects.filter(receiver = user_id,
    time__year=day_now.year,
    time__month=day_now.month,
    time__day=day_now.day)
    comments_today = models.Comment.objects.filter(receiver = user_id,
    time__year=day_now.year,
    time__month=day_now.month,
    time__day=day_now.day)

    messages_yesterday = models.Message.objects.filter(receiver = user_id,
    time__year=day_yesterday.year,
    time__month=day_yesterday.month,
    time__day=day_yesterday.day)
    comments_yesterday = models.Comment.objects.filter(receiver = user_id,
    time__year=day_yesterday.year,
    time__month=day_yesterday.month,
    time__day=day_yesterday.day)

    if messages_today or comments_today:
        for message in messages_today:
            topics_today.append(Notice(message.forum.id, 
            message.forum.name, message.time, 'message'))
        for comment in comments_today:
            topics_today.append(Notice(comment.new.id, 
            comment.new.title, comment.time, 'comment'))
    else:
        topics_today = 'Нет уведомлений'

    if messages_yesterday or comments_yesterday:
        for message in messages_yesterday:
            topics_yesterday.append(Notice(message.forum.id, 
            message.forum.name, message.time, 'message'))
        for comment in comments_yesterday:
            topics_yesterday.append(Notice(comment.new.id, 
            comment.new.title, comment.time, 'comment'))
    else:
        topics_yesterday = 'Нет уведомлений'
    
    if not topics_today == 'Нет уведомлений':
        topics_today: list = unique(topics_today)
        topics_today.sort(key=lambda date: datetime.strptime(date.time, '%H:%M'))

    if not topics_yesterday == 'Нет уведомлений':
        topics_yesterday: list = unique(topics_yesterday)
        topics_yesterday.sort(key=lambda date: datetime.strptime(date.time, '%H:%M'))
        
    return Notifications(topics_today, topics_yesterday)
