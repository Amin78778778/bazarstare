from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import db

router = Router()

@router.message(F.text == "🔗 Referal")
async def show_referral(message: Message):
    user_id = message.from_user.id
    bot_username = "BOTUNUZUN_USERNAME" # Botunuzun username-i
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    ref_count = await db.get_referral_count(user_id)

    await message.answer(
        f"🔗 **Referal Sistemi**\n\n"
        f"Sizin dəvət linkiniz:\n`{ref_link}`\n\n"
        f"👥 Dəvət etdiyiniz dost sayı: {ref_count}\n"
        f"💰 Hər dəvət üçün 30 xal qazanırsınız!",
        parse_mode="Markdown"
    )