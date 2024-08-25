import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import requests


# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = '6934206354:AAGyYYf86ZQNKHD83CBS4nqLDUkE6Z1yM3c'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я ваш новый Telegram бот. Чем могу помочь?")

    # Пример сохранения данных о пользователе в базе данных
    user_data = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    cursor.execute("INSERT OR IGNORE INTO users (id, username, first_name) VALUES (?, ?, ?)", user_data)
    conn.commit()


# Обработка команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = """
    Вот что я умею:
    /start - Начать общение с ботом
    /help - Показать это сообщение
    /weather - Получить прогноз погоды
    /news - Получить последние новости
    /rate - Узнать текущий курс валют
    """
    await message.reply(help_text, parse_mode=ParseMode.MARKDOWN)


# Пример команды для интеграции с API погоды
@dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    city = "Minsk"  # Замените на нужный город или парсите его из сообщения
    api_key = "YOUR_WEATHER_API_KEY"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        await message.reply(f"Погода в {city}: {weather_description}, температура: {temperature}°C")
    else:
        await message.reply("Не удалось получить данные о погоде. Попробуйте позже.")


# Пример команды для интеграции с API новостей
@dp.message_handler(commands=['news'])
async def get_news(message: types.Message):
    api_key = "YOUR_NEWS_API_KEY"
    news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    response = requests.get(news_url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        news_message = "Последние новости:\n\n"
        for article in articles[:5]:
            news_message += f"{article['title']}\n{article['url']}\n\n"
        await message.reply(news_message)
    else:
        await message.reply("Не удалось получить новости. Попробуйте позже.")


# Пример команды для интеграции с API курсов валют
@dp.message_handler(commands=['rate'])
async def get_exchange_rate(message: types.Message):
    base_currency = "USD"  # Базовая валюта
    target_currency = "BYN"  # Валюта, в которую нужно конвертировать
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        rate = data["rates"].get(target_currency)
        if rate:
            await message.reply(f"Курс {base_currency} к {target_currency}: {rate}")
        else:
            await message.reply("Не удалось получить курс валют. Попробуйте позже.")
    else:
        await message.reply("Не удалось получить данные о курсе валют. Попробуйте позже.")


# Обработка любого текстового сообщения
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"Вы написали: {message.text}")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
