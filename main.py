import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, PreCheckoutQuery
# Öz fayllarımızı import edirik
import db, admin, invest, dice_game, referal, extra, promo

# Bot tokeninizi bura daxil edin
TOKEN = "8853785671:AAE0SFxwUjmxhQrzXFCZNpqNdveb5CaTB9I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Router-ləri əlavə edirik
dp.include_router(admin.router)
dp.include_router(invest.router)
dp.include_router(dice_game.router)
dp.include_router(referal.router)
dp.include_router(extra.router)
dp.include_router(promo.router)

# --- ÖDƏNİŞ SİSTEMİ (Telegram Stars üçün) ---

@dp.pre_checkout_query()
async def on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@dp.message(F.successful_payment)
async def on_successful_payment(message: Message):
    # Ödəniş uğurlu olduqda ediləcək əməliyyatlar
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    
    # Məsələn, planı aktivləşdirmək (db.py-dəki funksiyanız)
    # await db.buy_plan_and_add_points(user_id, payload, 100) 
    
    await message.answer("✅ Ödəniş uğurla təsdiqləndi! Xallarınız balansınıza əlavə edildi.")

# --- BOTU İŞƏ SALMAQ ---

async def main():
    # Baza cədvəllərini başlat
    await db.init_db()
    # Botu işə sal
    print("Bot işə düşdü...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())