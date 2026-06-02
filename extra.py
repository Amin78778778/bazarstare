from aiogram import Router, F
from aiogram.types import Message
import db, random
from datetime import datetime, timedelta

router = Router()

# GÜNDƏLİK BONUS
@router.message(F.text == "🎁 Gündəlik Bonus")
async def daily_bonus(message: Message):
    user_id = message.from_user.id
    
    # Sadələşdirilmiş versiya:
    bonus = random.randint(50, 500)
    await db.add_points(user_id, bonus)

    await message.answer(f"🎁 Təbriklər! Gündəlik bonus olaraq {bonus} xal qazandınız.")

# NFT LOTEREYA
@router.message(F.text == "🎟 NFT Lotereya")
async def nft_lottery(message: Message):
    text = (
        "🎟 **NFT Lotereya**\n\n"
        "Qaydalar: Hər bilet 7 Star dəyərindədir.\n"
        "Cəmi: 100 bilet.\n"
        "Mükafat: [SwagBag NFT](https://t.me/nft/swagbag-87847)\n\n"
        "İştirak etmək üçün bilet alın!"
    )
    await message.answer(text, parse_mode="Markdown")