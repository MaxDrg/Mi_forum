import logging
import secrets
import string
import hashlib
import requests
from url import Web
from states import States
from config import Config
from buttons import Button
from database import Database
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configure logging
logging.basicConfig(level=logging.INFO)
cfg = Config()
btn = Button()
db = Database()

@cfg.dp.message_handler(commands="start")
async def start(message: types.Message):
    if not await db.check_user(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await cfg.bot.send_message(message.from_user.id, "Привет :)\nДля авторизации на форуме нужно перейти по ссылке.\n" + 
        "Ссылка одноразовая, так что, если ты зайдёшь с нового устройства, нужно будет получить новую ссылку",
        reply_markup=btn.markup_link)
    else:
        await cfg.bot.send_message(message.from_user.id, "Снова привет :)\nДля авторизации на форуме нужно перейти по ссылке.\n" + 
        "Ссылка одноразовая, так что, если ты зайдёшь с нового устройства, нужно будет получить новую ссылку",
        reply_markup=btn.markup_link)

@cfg.dp.message_handler(lambda message: message.text == 'Получить ссылку') 
async def get_link(message: types.Message):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(50))

    user_name = message.from_user.username
    
    photo = await message.from_user.get_profile_photos(0)
    file_info = await cfg.bot.get_file(photo.photos[0][0].file_id)

    files = {'media_file': (await cfg.bot.download_file(file_info.file_path))}
    param = {"user_id": message.from_user.id}
    requests.post(cfg.url, data=param, files=files)

    await db.update_user_data(
        user_id=message.from_user.id, 
        user_name=user_name,
        password=hashlib.sha256(password.encode('utf-8')).hexdigest()
    )

    web = Web(message.from_user.id)
    link = InlineKeyboardMarkup().add(InlineKeyboardButton('Перейти', url=await web.forum_url(password)))

    await cfg.bot.send_message(message.from_user.id, "Ваша ссылка для авторизации:", reply_markup=link)

@cfg.dp.message_handler(lambda message: message.text == 'Подписка') 
async def set_subscription(message: types.Message):
    subscription = await db.get_subscription(message.from_user.id)
    if subscription:
        subscription = f"\n\nВаша подписка действует до {subscription.strftime('%d/%m/%y')}"
    else:
        subscription = ''
    await cfg.bot.send_message(message.from_user.id, "Выберите срок подписки:" +
    "\n\n1 месяц = 10$\n3 месяца = 30$\n12 месяцев = 100$" + subscription,
    reply_markup=btn.markup_subscribe)
    await States.set_subscription.set()

@cfg.dp.message_handler(state=States.set_subscription) 
async def set_subscription(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться назад':
        await cfg.bot.send_message(message.from_user.id, "Вы в главном меню",
        reply_markup=btn.markup_link)
        await state.finish()
    elif message.text == '1 Месяц':
        days = 30
        web = Web(message.from_user.id)
        await cfg.bot.send_message(message.from_user.id, "Here 1")

        message_id = await db.get_message(message.from_user.id)
        if message_id:
            try:
                await cfg.bot.delete_message(message.from_user.id, message_id[1])
            except:
                pass
            await db.delete_transaction(message_id[0])

        await cfg.bot.send_message(message.from_user.id, "Here 2")

        transaction_id = await db.create_transaction(message.from_user.id, days)
        url, signature = await web.pay_url(transaction_id, days)

        await cfg.bot.send_message(message.from_user.id, "Here 3")

        link = InlineKeyboardMarkup().add(InlineKeyboardButton('Оплатить', url=url))
        send_message = await cfg.bot.send_message(message.from_user.id, 
        "Ваша ссылка для оплаты:", reply_markup=link)

        await db.update_transaction(transaction_id, send_message.message_id, signature)

        await cfg.bot.send_message(message.from_user.id, "Вы в главном меню",
        reply_markup=btn.markup_link)
        await state.finish()
    elif message.text == '3 Месяца':
        days = 92
        web = Web(message.from_user.id)
        await cfg.bot.send_message(message.from_user.id, "Here 1")

        message_id = await db.get_message(message.from_user.id)
        if message_id:
            try:
                await cfg.bot.delete_message(message.from_user.id, message_id[1])
            except:
                pass
            await db.delete_transaction(message_id[0])

        await cfg.bot.send_message(message.from_user.id, "Here 2")

        transaction_id = await db.create_transaction(message.from_user.id, days)
        url, signature = await web.pay_url(transaction_id, days)

        await cfg.bot.send_message(message.from_user.id, "Here 3")

        link = InlineKeyboardMarkup().add(InlineKeyboardButton('Оплатить', url=url))
        send_message = await cfg.bot.send_message(message.from_user.id, 
        "Ваша ссылка для оплаты:", reply_markup=link)

        await db.update_transaction(transaction_id, send_message.message_id, signature)

        await cfg.bot.send_message(message.from_user.id, "Вы в главном меню",
        reply_markup=btn.markup_link)
        await state.finish()
    elif message.text == '12 Месяцев':
        days = 365
        web = Web(message.from_user.id)
        await cfg.bot.send_message(message.from_user.id, "Here 1")

        message_id = await db.get_message(message.from_user.id)
        if message_id:
            try:
                await cfg.bot.delete_message(message.from_user.id, message_id[1])
            except:
                pass
            await db.delete_transaction(message_id[0])

        await cfg.bot.send_message(message.from_user.id, "Here 2")

        transaction_id = await db.create_transaction(message.from_user.id, days)
        url, signature = await web.pay_url(transaction_id, days)

        await cfg.bot.send_message(message.from_user.id, "Here 3")

        link = InlineKeyboardMarkup().add(InlineKeyboardButton('Оплатить', url=url))
        send_message = await cfg.bot.send_message(message.from_user.id, 
        "Ваша ссылка для оплаты:", reply_markup=link)

        await db.update_transaction(transaction_id, send_message.message_id, signature)

        await cfg.bot.send_message(message.from_user.id, "Вы в главном меню",
        reply_markup=btn.markup_link)
        await state.finish()

# @cfg.dp.message_handler(commands="start")
# async def Start(message: types.Message):
#     await cfg.bot.send_message(message.from_user.id, "hello")
#     photo = await message.from_user.get_profile_photos(0)
#     await cfg.bot.send_photo(message.from_user.id, photo.photos[0][0].file_id)
#     file_info = await cfg.bot.get_file(photo.photos[0][0].file_id)
#     new_photo = (await cfg.bot.download_file(file_info.file_path)).read()
#     
#     m = memoryview(new_photo)
# 
#     ##await cfg.bot.send_photo(message.from_user.id, f'{len(new_photo.read())}')
#     image = Image.open(io.BytesIO(new_photo))
#     image.save('test.jpg')
#     await db.add_user(message.from_user.id, m)
#     # await db.add_user(message.from_user.id, new_photo)
#     #print(new_photo)
# 
# @cfg.dp.message_handler(commands="show")
# async def Start(message: types.Message):
#     image = await db.show_photo()
#     print(type(image))
#     Image.open(io.BytesIO(image)).save('test.jpg')

if __name__ == "__main__":
    executor.start_polling(cfg.dp, skip_updates=True)