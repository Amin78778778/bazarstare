import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Öz fayllarımızı import edirik
import db, keyboards, admin, invest, dice_game, referal, extra, promo

# Bot tokeninizi bura daxil edin
TOKEN = "8853785671:AAE0SFxwUjmxhQrzXFCZNpqNdveb5CaTB9I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Router-ləri əlavə edirik (Bot bu fayllardakı əmrləri anlayacaq)
dp.include_router(admin.router)
dp.include_router(invest.router)
dp.include_router(dice_game.router)
dp.include_router(referal.router)
dp.include_router(extra.router)
dp.include_router(promo.router)

@dp.message(Command("start"))
async def start(message: Message):
    args = message.text.split()
    user_id = message.from_user.id

    # Referal məntiqi (əgər linklə gəlibsə)
    if len(args) > 1 and args[1].isdigit():
        inviter_id = int(args[1])
        if inviter_id != user_id:
            await db.add_points(user_id, 30)
            await db.add_points(inviter_id, 30)
            await db.set_referral(user_id, inviter_id)
            try:
                await bot.send_message(inviter_id, "🎉 Yeni referalınız var! +30 xal qazandınız.")
            except:
                pass

    # İstifadəçini bazaya əlavə edirik (əgər yoxdursa)
    await db.init_db() # Baza mövcuddursa sadəcə yoxlayacaq

    await message.answer("Xoş gəlmisiniz! Botun əsas menyusu:", reply_markup=keyboards.main_menu())

async def main():
    # Bazanı işə sal
    await db.init_db()

    # Botu işə sal
    print("Bot işə düşdü...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot dayandırıldı.")

# main.py faylına əlavə edin:
@dp.message(F.successful_payment)
async def on_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    
    # Payload-dan hansı planın alındığını bilirik (məsələn: buy_bronz)
    plan_name = payload.split("_")[1] 
    
    # db.py faylınızda planı aktivləşdirən funksiyanızı çağırın
    # await db.update_user_plan(user_id, plan_name) 
    
    await message.answer(f"✅ Ödəniş uğurlu oldu! {plan_name.upper()} planınız aktivləşdi.")
