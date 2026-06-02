import asyncio
import os
from aiogram import Bot, Dispatcher
import db  # db.py faylının eyni qovluqda olduğundan əmin ol

# Tokeni birbaşa qeyd edirik (istəsən sonradan os.getenv("TOKEN") edə bilərsən)
TOKEN = "8853785671:AAF6KXLRBKsif9mnUXUhBJu5-S8gupXBGRQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("Bot işə düşür...")
    
    # 1. Bazanı inisializasiya et
    await db.init_db()
    
    # 2. Köhnə bağlantıları təmizlə ki, 'ConflictError' verməsin
    await bot.delete_webhook(drop_pending_updates=True)
    
    # 3. Botu işə sal
    print("Bot aktivdir!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot dayandırıldı.")
