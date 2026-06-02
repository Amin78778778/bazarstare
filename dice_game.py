from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import db, random

router = Router()

def dice_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Zər At", callback_data="roll_dice")],
        [InlineKeyboardButton(text="⭐ Premium Zər (10 Star)", callback_data="buy_premium_dice")]
    ])
    return kb

@router.message(F.text == "🎲 Zər Oyunları")
async def show_dice_game(message: Message):
    await message.answer("Gündəlik 10 pulsuz zər haqqınız var!\n\nHər zər atışında nəticənin 2 qatını xal olaraq qazanırsınız.", reply_markup=dice_menu())

@router.callback_query(F.data == "roll_dice")
async def roll_dice(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    # Bazadan zər limitini yoxlayın (db.get_user_dice_count(user_id) lazımdır)
    # limit = await db.get_dice_count(user_id)
    
    # Sadələşdirilmiş nümunə:
    dice_result = await callback.message.answer_dice(emoji="🎲")
    value = dice_result.dice.value # Zərin nəticəsi (1-6)
    points_earned = value * 2
    
    await db.add_points(user_id, points_earned)
    await callback.message.answer(f"🎲 Zər nəticəsi: {value}\n✅ Qazandığınız xal: {points_earned}")
    await callback.answer()