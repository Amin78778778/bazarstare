from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import db

router = Router()
ADMIN_IDS = [123456789] # Admin ID-lərinizi bura yazın

# ADMIN: Yeni promokod yarat
@router.message(Command("newpromo"))
async def new_promo(message: Message):
    if message.from_user.id not in ADMIN_IDS: return
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Format: /newpromo [KOD] [xal]")
        return
    await db.create_promo(args[1].upper(), int(args[2]))
    await message.answer(f"✅ {args[1]} promokodu yaradıldı!")

# ADMIN: Promokod sil
@router.message(Command("delpromo"))
async def del_promo(message: Message):
    if message.from_user.id not in ADMIN_IDS: return
    args = message.text.split()
    await db.delete_promo(args[1].upper())
    await message.answer(f"❌ {args[1]} promokodu ləğv edildi.")

# İSTİFADƏÇİ: Promokodu yoxla (əgər kod heç bir əmr deyilsə, bot onu mesaj kimi qəbul edir)
@router.message(F.text)
async def check_promo(message: Message):
    code = message.text.upper()
    promo = await db.get_promo(code)
    
    if promo:
        reward = promo[0]
        await db.add_points(message.from_user.id, reward)
        await db.delete_promo(code) # Bir dəfəlik istifadə üçün sildik
        await message.answer(f"🎉 Təbriklər! Promokod aktivdir. Balansınıza {reward} xal əlavə olundu.")
    else:
        # Əgər əmr deyilsə və promokod da deyilsə, sadəcə susur və ya xəta verir
        pass