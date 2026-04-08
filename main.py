import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web

# MA'LUMOTLAR
TOKEN = "8680935840:AAEDW301uyvHMfdLkL44Gnmcy8GYCp-ytDU"
WEB_APP_URL = "https://yusufkhanakh.github.io/ususfxonpro-yuk-markazi-boti/"

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Railway "Crashed" xatosini oldini olish uchun oddiy Veb-Server
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Railway PORT ni o'zi beradi, agar bermasa 8080 ishlatiladi
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Health check server started on port {port}")

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚚 Yuklarni Boshqarish", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="📢 Kanalimiz", url="https://t.me/YusufxonPro_YukMarkazi")]
    ])
    await message.answer(
        f"<b>Salom, {message.from_user.first_name}!</b>\n\nYusufxonPro Logistics tizimi tayyor. Profilingizni ulab ishingizni boshlang.", 
        parse_mode="HTML", 
        reply_markup=markup
    )

async def main():
    # Bir vaqtning o'zida ham botni, ham veb-serverni ishga tushiramiz
    await asyncio.gather(
        dp.start_polling(bot),
        start_web_server()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
