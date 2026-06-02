from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="📋 Tapşırıqlar"), KeyboardButton(text="👤 Profil")],
        [KeyboardButton(text="🏆 Liderlər"), KeyboardButton(text="💰 Yatırım")],
        [KeyboardButton(text="🎲 Zər Oyunları"), KeyboardButton(text="🔗 Referal")],
        [KeyboardButton(text="🎁 Gündəlik Bonus"), KeyboardButton(text="🎟 NFT Lotereya")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)