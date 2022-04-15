from . import models
import secrets
import hashlib
import string

class Authorization:
    def __init__(self, user_id: str, passw: str) -> None:
        self.__user_id = user_id
        self.__passw = passw
        self.__current_user = None

        response = False
        db = models.User

        if db.objects.filter(telegr_id=self.__user_id).count():
            self.__current_user = db.objects.get(telegr_id=self.__user_id)
            if hashlib.sha256(self.__passw.encode('utf-8')).hexdigest() == self.__current_user.passw:
                response = True
            
        self.response = response

    def update_pass(self):
        if self.response:
            alphabet = string.ascii_letters + string.digits
            new_passw = ''.join(secrets.choice(alphabet) for i in range(50))
            self.__current_user.passw = new_passw
            self.__current_user.save()
            print(new_passw)
            return new_passw
        return None
        
