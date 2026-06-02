from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
import db
import asyncio

router = Router()
ADMIN_IDS = [6229739140] # ID-nizi bura yazın

# STATİSTİKA
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS: return

    user_count = await db.get_total_users()
    await message.answer(f"📊 **Bot Statistikası:**\n\n👥 Ümumi istifadəçi sayı: {user_count}")

# TOPLU MESAJ (BROADCAST)
@router.message(Command("broadcast"))
async def broadcast(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS: return

    # Komanda formatı: /broadcast Mesajınız
    text = message.text.replace("/broadcast ", "")
    users = await db.get_all_user_ids()

    sent = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            sent += 1
            await asyncio.sleep(0.05) # Botun ban yeməməsi üçün yavaş göndəririk
        except:
            continue

    await message.answer(f"✅ Mesaj {sent} istifadəçiyə uğurla göndərildi.")

@router.message(Command("giveplan"))
async def give_plan(message: Message):
    if message.from_user.id not in ADMIN_IDS: return
    args = message.text.split()
    # Format: /giveplan [userid] [plan]
    target_id, plan = args[1], args[2]

    await db.update_user_plan(int(target_id), plan)
    await message.answer(f"✅ {target_id} ID-li istifadəçiyə {plan} planı hədiyyə olundu.")

    try:
        await message.bot.send_message(target_id, f"🎉 Təbriklər! Admin tərəfindən sizə {plan} planı hədiyyə olundu.")
    except:
        pass