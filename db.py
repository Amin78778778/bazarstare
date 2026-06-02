import aiosqlite

# Bazanı başlatma və cədvəlləri yaratma
async def init_db():
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS promocodes
            (code TEXT PRIMARY KEY, reward INTEGER)""")
        # 'users' cədvəli yoxdursa yarat
        await db.execute("""CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0, plan TEXT DEFAULT 'Yoxdur', dice_count INTEGER DEFAULT 10, referred_by INTEGER)""")
        await db.commit()

async def create_promo(code, reward):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("INSERT OR REPLACE INTO promocodes (code, reward) VALUES (?, ?)", (code, reward))
        await db.commit()

async def delete_promo(code):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("DELETE FROM promocodes WHERE code = ?", (code,))
        await db.commit()

async def get_promo(code):
    async with aiosqlite.connect("bot_data.db") as db:
        async with db.execute("SELECT reward FROM promocodes WHERE code = ?", (code,)) as cursor:
            return await cursor.fetchone()

async def add_points(user_id: int, amount: int):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (id, points) VALUES (?, 0)", (user_id,))
        await db.execute("UPDATE users SET points = points + ? WHERE id = ?", (amount, user_id))
        await db.commit()

async def remove_points(user_id: int, amount: int):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("UPDATE users SET points = points - ? WHERE id = ?", (amount, user_id))
        await db.commit()

async def get_top_users():
    async with aiosqlite.connect("bot_data.db") as db:
        async with db.execute("SELECT id, points FROM users ORDER BY points DESC LIMIT 15") as cursor:
            return await cursor.fetchall()

async def get_user_profile(user_id):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (id, points, plan, dice_count) VALUES (?, 0, 'Yoxdur', 10)", (user_id,))
        await db.commit()
        async with db.execute("SELECT points, plan, dice_count FROM users WHERE id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def update_user_plan(user_id, plan):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("UPDATE users SET plan = ? WHERE id = ?", (plan, user_id))
        await db.commit()

async def buy_plan_and_add_points(user_id, plan_name, points_to_add):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("UPDATE users SET plan = ? WHERE id = ?", (plan_name, user_id))
        await db.execute("UPDATE users SET points = points + ? WHERE id = ?", (points_to_add, user_id))
        await db.commit()

async def get_dice_count(user_id):
    async with aiosqlite.connect("bot_data.db") as db:
        async with db.execute("SELECT dice_count FROM users WHERE id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def decrease_dice_count(user_id):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("UPDATE users SET dice_count = dice_count - 1 WHERE id = ?", (user_id,))
        await db.commit()

async def set_referral(user_id, inviter_id):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("UPDATE users SET referred_by = ? WHERE id = ?", (inviter_id, user_id))
        await db.commit()

async def get_referral_count(user_id):
    async with aiosqlite.connect("bot_data.db") as db:
        async with db.execute("SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0]

async def get_total_users():
    async with aiosqlite.connect("bot_data.db") as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            result = await cursor.fetchone()
            return result[0]