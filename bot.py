import os
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Получаем токен из переменных окружения (на Render ты добавишь его в Environment Variables)
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Загружаем задания из JSON-файла
with open("challenges.json", "r", encoding="utf-8") as f:
    challenges = json.load(f)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🎨 Привет! Я помогу тебе расти как художнику.\n\n"
        "Команды:\n"
        "/challenge — получить задание на сегодня\n"
        "/progress — загрузить свою работу"
    )

# Команда /challenge
@dp.message(Command("challenge"))
async def send_challenge(message: types.Message):
    challenge = random.choice(challenges)
    refs = "\n".join([f"🔗 {r}" for r in challenge["references"]])
    text = (
        f"✨ *Тема*: {challenge['theme']}\n"
        f"🎯 *Задание*: {challenge['task']}\n"
        f"💡 *Совет*: {challenge['tips']}\n\n"
        f"🖼 Референсы:\n{refs}"
    )
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# Команда /progress
@dp.message(Command("progress"))
async def ask_for_art(message: types.Message):
    await message.answer("Отправь мне изображение своей работы 👇")

# Обработка фото
@dp.message(types.ContentType.PHOTO)
async def save_art(message: types.Message):
    await message.answer("✅ Работа сохранена! Через 7 дней я покажу, как ты прогрессируешь.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())