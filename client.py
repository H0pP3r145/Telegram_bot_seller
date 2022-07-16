from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import psycopg2 as ps
import os
import json

with open('config.json') as file:
  stock = json.load(file)

base = ps.connect(os.environ.get('DATABASE_URL'), sslmode="require")
cur = base.cursor()

API_TOKEN = stock['API_TOKEN']
QIWI_TOKEN = stock['QIWI_TOKEN']
URL_APP = stock['URL_APP']
ADMIN_ID = stock['ADMIN_ID']

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
