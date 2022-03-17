import time

from aiogram import types
from aiogram.utils import executor
from aiogram.utils.exceptions import TelegramAPIError
from bot_data import dp, bot, ids
from ltscript import login_lt
from plscript import login_pl


@dp.message_handler(lambda msg: msg.from_user.id in ids and msg.text.startswith('/startlt') or msg.text.startswith('/startpl'))
async def start_bot(msg: types.Message):
    args = msg.text.split()
    try:
        delay = int(args[1])
    except Exception:
        delay = 3
    if args[0] == '/startlt':
        for id in ids:
            await bot.send_message(id, f'Скрипт [LT] запущен. Задежка - {delay} секунд.')
        await login_lt(delay)
    elif args[0] == '/startpl':
        for id in ids:
            await bot.send_message(id, f'Скрипт [PL] запущен. Задежка - {delay} секунд.')
        await login_pl(delay)


if __name__ == '__main__':
    while True:
        time.sleep(2)
        try:
            executor.start_polling(dp, skip_updates=True)
        except TelegramAPIError:
            print('No connect to server, check internet connection.')
