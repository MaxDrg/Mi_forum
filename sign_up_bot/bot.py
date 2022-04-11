import logging
import io
from PIL import Image
from config import Config
from database import Database
from buttons import Button
from aiogram import executor, types
from config import Config
from aiogram.dispatcher import FSMContext

# Configure logging
logging.basicConfig(level=logging.INFO)
cfg = Config()
btn = Button()
db = Database()

# first
@cfg.dp.message_handler(commands="start")
async def Start(message: types.Message):
    await cfg.bot.send_message(message.from_user.id, "hello")
    photo = await message.from_user.get_profile_photos(0)
    await cfg.bot.send_photo(message.from_user.id, photo.photos[0][0].file_id)
    file_info = await cfg.bot.get_file(photo.photos[0][0].file_id)
    new_photo = (await cfg.bot.download_file(file_info.file_path)).read()
    
    m = memoryview(new_photo)

    ##await cfg.bot.send_photo(message.from_user.id, f'{len(new_photo.read())}')
    image = Image.open(io.BytesIO(new_photo))
    image.save('test.jpg')
    await db.add_user(message.from_user.id, m)
    # await db.add_user(message.from_user.id, new_photo)
    #print(new_photo)

@cfg.dp.message_handler(commands="show")
async def Start(message: types.Message):
    image = await db.show_photo()
    print(type(image))
    Image.open(io.BytesIO(image)).save('test.jpg')

if __name__ == "__main__":
    executor.start_polling(cfg.dp, skip_updates=True)