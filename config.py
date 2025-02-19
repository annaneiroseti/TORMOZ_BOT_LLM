import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LLM_API_URL = os.getenv("LLM_API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
