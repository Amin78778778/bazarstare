import os
from aiogram import Bot, Dispatcher
import asyncio
import db

# Tokeni buraya birbaşa yapışdır (müvəqqəti olaraq)
TOKEN = "8853785671:AAF6KXLRBKsif9mnUXUhBJu5-S8gupXBGRQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    # 1. Bazanı avtomatik yaradır/yoxlayır
    print("Baza yoxlanılır...")
    await db.init_db()
    
    # 2. Botu işə salırıq
    print("Bot işə düşür...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
