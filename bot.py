import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import BOT_TOKEN, LLM_API_URL, MODEL_NAME

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    """Приветственное сообщение при старте."""
    greeting_text = "Приветствую!!! О, моё Величество! Я бот, немного тормоз, но быстро учусь! Чем могу служить?"
    await message.answer(greeting_text)


async def query_llm(prompt):
    """Функция для запроса к локальной модели LLM."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 200
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(LLM_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "Ошибка в ответе от модели")
    except requests.RequestException as e:
        logging.error(f"Ошибка запроса к LLM: {e}")
        return "Не удалось получить ответ от модели."


@dp.message()
async def handle_message(message: types.Message):
    """Обработчик всех входящих сообщений."""
    user_input = message.text
    response_text = await query_llm(user_input)
    await message.answer(response_text)


async def main():
    """Основная функция запуска бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
