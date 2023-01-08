import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
ids = ["list of admins id"]
dp = Dispatcher(bot)




