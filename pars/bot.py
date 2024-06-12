import json

from aiogram import Bot, Dispatcher, executor, types
from config import token
from main import check_new_update
from aiogram.dispatcher.filters import Text


bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands = 'start')
async  def start (message: types.Message):
    start_button = ['Все видео', 'Свежие видео']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer('Лента новостей',reply_markup=keyboard)

@dp.message_handler(Text(equals='Все видео'))
async  def get_all_video(message: types.Message):
    with open('dict.json') as file:
        data_dict = json.load(file)
    for k,v in sorted(data_dict.items()):
        video = f'{v["date"]}\n'\
                f'{v["link"]}\n'
        await message.answer(video)

@dp.message_handler(Text(equals='Свежие видео'))
async  def get_all_video(message: types.Message):
    fresh_video = check_new_update()
    if len(fresh_video)>=1:
        for k, v in sorted(fresh_video.items()):
            video = f'{v["date"]}\n' \
                    f'{v["link"]}\n'
            await message.answer(video)
    else:
        await message.answer('Пока ничего нет')





if __name__ == '__main__':
    executor.start_polling(dp)