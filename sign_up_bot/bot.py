import logging
import secrets
import string
import hashlib
import requests
import io
from PIL import Image
from url import Web
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
        await db.add_user(message.from_user.id)
        await cfg.bot.send_message(message.from_user.id, "Привет :)\nДля авторизации на форуме нужно перейти по ссылке.\n" + 
        "Ссылка одноразовая, так что, если ты зайдёшь с нового устройства, нужно будет получить новую ссылку",
        reply_markup=btn.markup_link)

@cfg.dp.message_handler(lambda message: message.text == 'Получить ссылку') 
async def get_link(message: types.Message):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(50))

    user_name = message.from_user.first_name
    if not message.from_user.username == None:
        user_name = message.from_user.username

    photo = await message.from_user.get_profile_photos(0)
    file_info = await cfg.bot.get_file(photo.photos[0][0].file_id)
    user_image =  (await cfg.bot.download_file(file_info.file_path)).read()
    image = Image.open(io.BytesIO(user_image))

    files = {'media': user_image}
    requests.post(cfg.url, files=files)

    await db.update_user_data(
        user_id=message.from_user.id, 
        user_name=user_name,
        password=hashlib.sha256(password.encode('utf-8')).hexdigest()
    )

    web = Web(message.from_user.id, password)
    link = InlineKeyboardMarkup().add(InlineKeyboardButton('Перейти', url=web.url))

    await cfg.bot.send_message(message.from_user.id, "Ваша ссылка для авторизации:", reply_markup=link)

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