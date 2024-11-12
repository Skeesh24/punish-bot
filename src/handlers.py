import asyncio
from datetime import datetime, timedelta
from os import getenv

from aiogram import Bot, Dispatcher, types

from database import get_user_words_count, update_user_words_count

IDS_TO_LIMIT = ["688962669", "2050790028"]
BOT_TOKEN = getenv("BOT_TOKEN")
BAN_MINUTES = getenv("BAN_MINUTES")

# Объект бота
bot = Bot(token=BOT_TOKEN)

# Диспетчер
dp = Dispatcher()


# Хэндлер на все сообщения
@dp.message()
async def cmd_common(message: types.Message):
    if str(message.from_user.id) in IDS_TO_LIMIT and message.text:

        words_count = get_user_words_count(message.from_user.id)
        limit = words_count - len(message.text.split())

        update_user_words_count(
            message.from_user.id,
            limit,
        )

        reply_text = "Остаток слов: %d." % limit

        if limit <= 0:
            reply_text = (
                "Вы забанены на %s минут. Причина: превышение лимита слов."
                % BAN_MINUTES
            )
            await message.reply(reply_text)
            await asyncio.sleep(2)
            await bot.ban_chat_member(
                message.chat.id,
                message.from_user.id,
                until_date=datetime.now() + timedelta(minutes=int(BAN_MINUTES)),
            )
            update_user_words_count(
                message.from_user.id,
            )
            return

        await message.reply(reply_text)
