import asyncio
import os
from aiogram import Bot, Dispatcher
import db

# Tokeni birbaşa bura yazırıq (Daha sadə olsun deyə)
TOKEN = "8853785671:AAF6KXLRBKsif9mnUXUhBJu5-S8gupXBGRQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("Bot işə düşür...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
