import asyncio
import logging

from dotenv import load_dotenv

from handlers import bot, dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


# Запуск процесса поллинга новых апдейтов
async def main():
    logger.info("Connecting to Telegram API...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Bot is starting...")
    asyncio.run(main())
