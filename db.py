import os
import asyncpg
from dotenv import load_dotenv

# Əgər .env faylı istifadə edirsənsə, bunu aktiv saxla
load_dotenv()

# Railway-dəki Variables hissəsindən DATABASE_URL-i oxuyur
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_connection():
    """Bazaya qoşulmaq üçün istifadə olunur."""
    try:
        if not DATABASE_URL:
            print("XƏTA: DATABASE_URL təyin olunmayıb!")
            return None
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        print(f"Bazaya qoşulma xətası: {e}")
        return None

async def init_db():
    """Bazanı inisializasiya etmək (cədvəlləri yaratmaq) üçün."""
    conn = await get_connection()
    if conn:
        try:
            # Buraya öz cədvəllərini yaratma kodunu yaza bilərsən
            # Məsələn:
            # await conn.execute("CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY);")
            print("Bazaya uğurla qoşuldu və inisializasiya olundu.")
        finally:
            await conn.close()
