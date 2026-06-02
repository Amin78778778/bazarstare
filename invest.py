from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LabeledPrice
import db

router = Router()

# Planların qiymətləri (Amount: 50 Star = 50, 100 Star = 100, 200 Star = 200)
PLANS = {
    "buy_bronz": {"title": "🥉 Bronz Planı", "amount": 50, "description": "100 xal/gün"},
    "buy_silver": {"title": "🥈 Gümüş Planı", "amount": 100, "description": "150 xal/gün"},
    "buy_gold": {"title": "🥇 Qızıl Planı", "amount": 200, "description": "250 xal/gün"}
}

def invest_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥉 Bronz (50 Star)", callback_data="buy_bronz")],
        [InlineKeyboardButton(text="🥈 Gümüş (100 Star)", callback_data="buy_silver")],
        [InlineKeyboardButton(text="🥇 Qızıl (200 Star)", callback_data="buy_gold")]
    ])
    return kb

@router.message(F.text == "💰 Yatırım")
async def show_invest(message: Message):
    await message.answer("Sizə uyğun yatırım planını seçin:", reply_markup=invest_menu())

@router.callback_query(F.data.startswith("buy_"))
async def process_invest(callback: CallbackQuery):
    plan_key = callback.data
    plan = PLANS.get(plan_key)

    if plan:
        # Telegram Stars üçün invoice göndəririk
        await callback.message.bot.send_invoice(
            chat_id=callback.from_user.id,
            title=plan["title"],
            description=plan["description"],
            payload=plan_key,  # Hansı planın alındığını bura qeyd edirik
            currency="XTR",    # Telegram Stars valyutası
            prices=[LabeledPrice(label=plan["title"], amount=plan["amount"])]
        )

    await callback.answer()
