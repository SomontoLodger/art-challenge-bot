import os
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

with open("challenges.json", "r", encoding="utf-8") as f:
    challenges = json.load(f)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "🎨 Привет! Я помогу тебе расти как художнику.\n\n"
        "Команды:\n"
        "/challenge — получить задание на сегодня\n"
        "/progress — загрузить свою работу"
    )

@dp.message_handler(commands=['challenge'])
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

@dp.message_handler(commands=['progress'])
async def ask_for_art(message: types.Message):
    await message.answer("Отправь мне изображение своей работы 👇")

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def save_art(message: types.Message):
    await message.answer("✅ Работа сохранена! Через 7 дней я покажу, как ты прогрессируешь.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling())