from . import models
import secrets
import hashlib
import string

class Authorization:
    def __init__(self, user_id: str, passw: str, from_bot: bool = False) -> None:
        self.__user_id = user_id
        self.__passw = passw
        self.__from_bot = from_bot

        response = False
        db = models.User

        if db.objects.filter(telegr_id=self.__user_id).count():
            current_user = db.objects.get(telegr_id=self.__user_id)
            if hashlib.sha256(self.__passw.encode('utf-8')).hexdigest() == current_user.passw:
                if self.__from_bot:
                    alphabet = string.ascii_letters + string.digits
                    new_passw = ''.join(secrets.choice(alphabet) for i in range(50))
                    current_user.passw = new_passw
                    current_user.save()
                response = True
            
        self.response = response
