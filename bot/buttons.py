from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class Button:
    def __init__(self):
        button_link = KeyboardButton('Получить ссылку')
        button_subscribe = KeyboardButton('Подписка')
        self.markup_link = ReplyKeyboardMarkup(resize_keyboard=True).row(button_link).row(button_subscribe)

        button_back = KeyboardButton('Вернуться назад')
        self.markup_back = ReplyKeyboardMarkup(resize_keyboard=True).row(button_back)

        button_month1 = KeyboardButton('1 Месяц')
        button_month3 = KeyboardButton('3 Месяца')
        button_month12 = KeyboardButton('12 Месяцев')
        self.markup_subscribe = ReplyKeyboardMarkup(resize_keyboard=True).row(button_month1, 
        button_month3, button_month12).row(button_back)