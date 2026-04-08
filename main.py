import asyncio
import logging
import os
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web

# --- SOZLAMALAR ---
TOKEN = "8680935840:AAEDW301uyvHMfdLkL44Gnmcy8GYCp-ytDU"  # Sening bot tokining
ADMIN_ID = 619827354  # Sening Telegram ID raqaming
CHANNELS = ["@YusufxonPro_YukMarkazi", "@YusufxonPro_Yangiliklar"] # Tekshiriladigan kanallar

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. Kanallarga obuna bo'lganini tekshirish funksiyasi
async def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception:
            return False
    return True

# 2. WebApp API (HTML'dagi fetch orqali keladigan ma'lumotlar)
async def handle_webapp_api(request):
    try:
        data = await request.json()
        
        # Adminga Face ID va Login haqida hisobot yuborish
        report = (
            f"👑 <b>YANGI PREMIUM KIRISH:</b>\n\n"
            f"👤 F.I: {data.get('name')} {data.get('surname')}\n"
            f"📞 Tel: {data.get('phone')}\n"
            f"🆔 User: @{data.get('username')}\n"
            f"✅ <b>Face ID va Xavfsizlik tasdiqlandi!</b>"
        )
        await bot.send_message(ADMIN_ID, report, parse_mode="HTML")
        return web.json_response({"status": "ok"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

# 3. Start komandasi (Obunani tekshiradi)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    
    if is_subscribed:
        # Agar obuna bo'lgan bo'lsa, WebApp tugmasini ko'rsatadi
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🚀 PREMIUMGA KIRISH", 
                web_app=WebAppInfo(url="https://yusufxonpro.uz") # Sening sayting linki
            )]
        ])
        await message.answer(
            f"Xush kelibsiz, {message.from_user.first_name}!\n"
            f"Siz Premium tizimimizga a'zosiz. Quyidagi tugma orqali kiring:",
            reply_markup=kb
        )
    else:
        # Obuna bo'lmagan bo'lsa, kanallarga yo'naltiradi
        kb_list = []
        for ch in CHANNELS:
            kb_list.append([InlineKeyboardButton(text=f"Kanalga a'zo bo'lish", url=f"https://t.me/{ch[1:]}")])
        kb_list.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")])
        
        await message.answer(
            "Tizimdan foydalanish va Premium statusni olish uchun kanallarimizga obuna bo'ling:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_list)
        )

# 4. Obunani qayta tekshirish (Tugma bosilganda)
@dp.callback_query(F.data == "check_sub")
async def callback_check(callback: types.CallbackQuery):
    if await check_subscription(callback.from_user.id):
        await callback.answer("Rahmat! Endi /start bosing.", show_alert=True)
    else:
        await callback.answer("Hali hamma kanallarga a'zo emassiz!", show_alert=True)

# 5. WebApp orqali yuborilgan ma'lumotlarni qabul qilish (tg.sendData)
@dp.message(F.web_app_data)
async def web_app_receive(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    # Yuk haqidagi ma'lumotni barcha kanallarga tarqatish
    post_text = (
        f"📦 <b>YANGI PREMIUM YUK!</b>\n\n"
        f"📝 Ma'lumot: {data.get('desc')}\n"
        f"📞 Aloqa: {data.get('phone')}\n"
        f"👤 Mas'ul: @{message.from_user.username}"
    )
    
    for channel in CHANNELS:
        await bot.send_message(channel, post_text, parse_mode="HTML")
    
    await message.answer("✅ Ma'lumotlaringiz barcha kanallarga muvaffaqiyatli tarqatildi!")

# --- RAILWAY VA SERVER QISMI ---
async def main():
    # Aiohttp serverini sozlash
    app = web.Application()
    app.router.add_post('/api/verify', handle_webapp_api)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Railway'da PORT o'zgaruvchisi muhim
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    # Bot va Serverni birga ishga tushirish
    await asyncio.gather(
        site.start(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
