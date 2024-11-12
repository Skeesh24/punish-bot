import asyncio

from dotenv import load_dotenv

from handlers import bot, dp

load_dotenv()


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
