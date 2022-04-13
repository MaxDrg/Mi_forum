from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class Button:
    def __init__(self):
        button_link = KeyboardButton('Получить ссылку')
        self.markup_link = ReplyKeyboardMarkup(resize_keyboard=True).row(button_link)

        button_back = KeyboardButton('Вернуться назад')
        self.markup_back = ReplyKeyboardMarkup(resize_keyboard=True).row(button_back)