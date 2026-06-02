import asyncpg
import os

# Railway-də 'Variables' hissəsində DATABASE_URL-i əlavə etməyi unutmayın
DATABASE_URL = os.environ.get("postgresql://postgres:IhlnSLcZaVFJnrGjUXipIhMwxlfXPYyh@postgres.railway.internal:5432/railway")

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

async def init_db():
    conn = await get_connection()
    await conn.execute("""CREATE TABLE IF NOT EXISTS promocodes
        (code TEXT PRIMARY KEY, reward INTEGER)""")
    await conn.execute("""CREATE TABLE IF NOT EXISTS users
        (id BIGINT PRIMARY KEY, points INTEGER DEFAULT 0, plan TEXT DEFAULT 'Yoxdur', dice_count INTEGER DEFAULT 10, referred_by BIGINT)""")
    await conn.close()

async def create_promo(code, reward):
    conn = await get_connection()
    await conn.execute("INSERT INTO promocodes (code, reward) VALUES ($1, $2) ON CONFLICT(code) DO UPDATE SET reward = $2", code, reward)
    await conn.close()

async def delete_promo(code):
    conn = await get_connection()
    await conn.execute("DELETE FROM promocodes WHERE code = $1", code)
    await conn.close()

async def get_promo(code):
    conn = await get_connection()
    row = await conn.fetchrow("SELECT reward FROM promocodes WHERE code = $1", code)
    await conn.close()
    return row

async def add_points(user_id: int, amount: int):
    conn = await get_connection()
    await conn.execute("INSERT INTO users (id, points) VALUES ($1, $2) ON CONFLICT(id) DO UPDATE SET points = users.points + $2", user_id, amount)
    await conn.close()

async def remove_points(user_id: int, amount: int):
    conn = await get_connection()
    await conn.execute("UPDATE users SET points = points - $1 WHERE id = $2", amount, user_id)
    await conn.close()

async def get_top_users():
    conn = await get_connection()
    rows = await conn.fetch("SELECT id, points FROM users ORDER BY points DESC LIMIT 15")
    await conn.close()
    return rows

async def get_user_profile(user_id):
    conn = await get_connection()
    await conn.execute("INSERT INTO users (id, points) VALUES ($1, 0) ON CONFLICT(id) DO NOTHING", user_id)
    row = await conn.fetchrow("SELECT points, plan, dice_count FROM users WHERE id = $1", user_id)
    await conn.close()
    return row

async def update_user_plan(user_id, plan):
    conn = await get_connection()
    await conn.execute("UPDATE users SET plan = $1 WHERE id = $2", plan, user_id)
    await conn.close()

async def buy_plan_and_add_points(user_id, plan_name, points_to_add):
    conn = await get_connection()
    await conn.execute("UPDATE users SET plan = $1, points = points + $2 WHERE id = $3", plan_name, points_to_add, user_id)
    await conn.close()

async def get_dice_count(user_id):
    conn = await get_connection()
    val = await conn.fetchval("SELECT dice_count FROM users WHERE id = $1", user_id)
    await conn.close()
    return val if val else 0

async def decrease_dice_count(user_id):
    conn = await get_connection()
    await conn.execute("UPDATE users SET dice_count = dice_count - 1 WHERE id = $1", user_id)
    await conn.close()

async def set_referral(user_id, inviter_id):
    conn = await get_connection()
    await conn.execute("UPDATE users SET referred_by = $1 WHERE id = $2", inviter_id, user_id)
    await conn.close()

async def get_referral_count(user_id):
    conn = await get_connection()
    count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1", user_id)
    await conn.close()
    return count

async def get_total_users():
    conn = await get_connection()
    count = await conn.fetchval("SELECT COUNT(*) FROM users")
    await conn.close()
    return count
