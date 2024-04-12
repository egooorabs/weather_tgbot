import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import tg_bot_token, open_weather_token

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    get_weather_button = KeyboardButton("/get_weather")
    help_button = KeyboardButton("/help")
    keyboard_markup.add(get_weather_button, help_button)
    await message.reply("Привет! Нажми на кнопку, чтобы получить погоду или помощь.", reply_markup=keyboard_markup)

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("Бот работает на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города боту")

@dp.message_handler(commands=["get_weather"])
async def get_weather_command(message: types.Message):
    await message.reply("Напиши название города, чтобы я прислал погоду.")

@dp.message_handler(content_types=["photo"])
async def handle_photo(message: types.Message):
    await message.reply("Спасибо за фото! Но, к сожалению, я его не смогу обработать:(")

@dp.message_handler(content_types=["video"])
async def handle_video(message: types.Message):
    await message.reply("Спасибо за видео! Но, к сожалению, я его не смогу обработать:(")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        wd = weather_description

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"***Хорошего дня!***"
              )

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)
