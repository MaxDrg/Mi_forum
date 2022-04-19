from django.db import models

class User(models.Model):
    telegr_id = models.BigIntegerField("Telegram's ID", unique=True)
    first_name = models.CharField("User's first name", max_length=255, null=False)
    user_name = models.CharField("User's name", max_length=255, null=True)
    passw = models.CharField("Password", max_length=255, null=True)
    subscription = models.DateTimeField("Subscription", null=True)
    image = models.ImageField("Profile's photo", default=None, null=True)

    def __str__(self):
        return f"ID: {self.telegr_id} Name: {self.first_name}"

class New(models.Model):
    title = models.CharField("Title", max_length=255 ,null=False)
    info = models.TextField("Information", null=False)
    pre_info = models.TextField("Pre-information", null=False)
    hashtags = models.TextField("Hashtags", null=False)
    date = models.DateField("Publication time", auto_now_add=True)
    image = models.ImageField("Image of news", default=None, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    message_text = models.TextField("Text of message", null=False)
    reply_to = models.BigIntegerField("ID of message reply", null=True, default=None)
    receiver = models.BigIntegerField("Telegram ID of message answer", null=True, default=None)
    time = models.DateTimeField("Time of sending", auto_now_add=True)
    new = models.ForeignKey(New, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    is_answer = models.BooleanField("Is answer", null=True, default=None)

    def __str__(self):
        return self.message_text

class Category(models.Model):
    name = models.CharField("Name of category", max_length=255)
    description = models.TextField("Categories description", null=True)

    def __str__(self):
        return self.name

class Forum(models.Model):
    name = models.CharField("Name of forum", max_length=255)
    description = models.TextField("Forums description", null=True)
    private = models.BooleanField("Is private")
    forum_text = models.TextField("Forums text", null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.forum_name

class Message(models.Model):
    message_text = models.TextField("Text of message", null=False)
    reply_to = models.BigIntegerField("ID of message reply", null=True, default=None)
    receiver = models.BigIntegerField("Telegram ID of message answer", null=True, default=None)
    time = models.DateTimeField("Time of sending", auto_now_add=True)
    forum = models.ForeignKey(Forum, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    is_answer = models.BooleanField("Is answer", null=True, default=None)

    def __str__(self):
        return self.message_text