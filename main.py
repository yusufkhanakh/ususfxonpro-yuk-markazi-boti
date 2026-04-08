import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web

# --- KONFIGURATSIYA ---
TOKEN = "8680935840:AAEDW301uyvHMfdLkL44Gnmcy8GYCp-ytDU"
ADMIN_ID = 619827354
CHANNEL_ID = "@YusufxonPro_YukMarkazi"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- WEBAPP MA'LUMOTLARINI QABUL QILISH (AIOHTTP) ---
async def handle_webapp_data(request):
    data = await request.json()
    
    # Adminga Face ID va Login haqida xabar
    await bot.send_message(
        ADMIN_ID,
        f"⚡️ <b>WEBAPP LOGIN (Face ID):</b>\n\n"
        f"👤 Ism: {data.get('name')}\n"
        f"📁 Familiya: {data.get('surname')}\n"
        f"📞 Tel: {data.get('phone')}\n"
        f"🆔 User: @{data.get('username')}\n"
        f"✅ Status: Kirish tasdiqlandi"
    )
    return web.json_response({"status": "ok"})

# --- BOT BUYRUQLARI (AIOGRAM) ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 TIZIMGA KIRISH", web_app=WebAppInfo(url="https://yusufxonpro.uz"))]
    ])
    await message.answer(f"Xush kelibsiz, {message.from_user.first_name}!", reply_markup=markup)

# Guruhga yangi odam qo'shilsa SANOQCHI
@dp.message(F.new_chat_members)
async def member_counter(message: types.Message):
    count = await bot.get_chat_member_count(message.chat.id)
    for member in message.new_chat_members:
        name = member.username if member.username else member.first_name
        await message.answer(
            f"🚀 Xush kelibsiz, @{name}!\n"
            f"Siz guruhimizning <b>{count}-chi</b> a'zosisiz!",
            parse_mode="HTML"
        )

# WebApp dan kelgan yuklarni kanalga chiqarish
@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    import json
    data = json.loads(message.web_app_data.data)
    
    text = (
        f"📦 <b>YANGI YUK!</b>\n\n"
        f"📝 Yuk: {data.get('desc')}\n"
        f"⏳ Muddat: {data.get('day')} kun\n"
        f"👤 Mas'ul: @{message.from_user.username}"
    )
    await bot.send_message(CHANNEL_ID, text, parse_mode="HTML")
    await message.answer("✅ Yuk kanalga joylandi!")

# --- RAILWAY UCHUN SERVERNI ISHGA TUSHIRISH ---
async def main():
    # Aiohttp serverini sozlash
    app = web.Application()
    app.router.add_post('/api/verify', handle_webapp_data)
    
    runner = web.AppRunner(app)
    await runner.setup()
    # Railway PORT ni avtomatik oladi, bo'lmasa 8080 ni ishlatadi
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    
    logging.info("Server va Bot ishga tushmoqda...")
    await asyncio.gather(
        site.start(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
