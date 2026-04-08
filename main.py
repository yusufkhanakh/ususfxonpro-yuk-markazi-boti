import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

# BOT TOKENINGIZ
TOKEN = "8680935840:AAEDW301uyvHMfdLkL44Gnmcy8GYCp-ytDU"
# GITHUB PAGES HAVOLANGIZ
WEB_APP_URL = "https://yusufkhanakh.github.io/ususfxonpro-yuk-markazi-boti/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Railway loglari uchun logging
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # WebApp ochish uchun tugma
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚚 Yuklarni Boshqarish", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [InlineKeyboardButton(
            text="📢 Kanalga o'tish", 
            url="https://t.me/YusufxonPro_YukMarkazi"
        )]
    ])
    
    await message.answer(
        f"<b>Assalomu alaykum, {message.from_user.first_name}!</b>\n\n"
        "YusufxonPro tizimiga xush kelibsiz. Profilingizni ulab yuk joylashni boshlang.",
        parse_mode="HTML",
        reply_markup=markup
    )

async def main():
    logging.info("Bot Railway-da ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
