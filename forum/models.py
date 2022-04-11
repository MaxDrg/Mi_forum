from django.db import models

class User(models.Model):
    telegr_id = models.BigIntegerField("Telegram's ID")
    user_name = models.CharField("User's name", max_length=255, null=True)
    passw = models.CharField("Password", max_length=255, null=True)
    subscription = models.DateTimeField("Subscription", null=True)
    image = models.ImageField("Profile's photo", default=None, null=True)