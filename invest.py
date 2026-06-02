from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import db

router = Router()

# Yatırım planları menyusu
def invest_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥉 Bronz (50 Star) - 100 xal/gün", callback_data="buy_bronz")],
        [InlineKeyboardButton(text="🥈 Gümüş (100 Star) - 150 xal/gün", callback_data="buy_silver")],
        [InlineKeyboardButton(text="🥇 Qızıl (200 Star) - 250 xal/gün", callback_data="buy_gold")]
    ])
    return kb

@router.message(F.text == "💰 Yatırım")
async def show_invest(message: Message):
    await message.answer("Sizə uyğun yatırım planını seçin:", reply_markup=invest_menu())

@router.callback_query(F.data.startswith("buy_"))
async def process_invest(callback: CallbackQuery):
    plan = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    # Bazada planı yeniləyirik (burada əslində 'Star' balansını da yoxlamalısınız)
    # db.update_user_plan(user_id, plan) 
    
    await callback.message.answer(f"✅ Uğurla {plan.upper()} planını aktivləşdirdiniz!")
    await callback.answer()