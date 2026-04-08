import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8680935840:AAEDW301uyvHMfdLkL44Gnmcy8GYCp-ytDU"
WEB_APP_URL = "https://yusufkhanakh.github.io/ususfxonpro-yuk-markazi-boti/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    # Tugma yaratish
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚚 Yuklarni bepul joylash", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [InlineKeyboardButton(
            text="📢 Kanalimizga o'ting", 
            url="https://t.me/YusufxonPro_YukMarkazi"
        )]
    ])
    
    await message.answer(
        f"<b>Assalomu alaykum, {message.from_user.first_name}!</b>\n\n"
        "YusufxonPro yuk markaziga xush kelibsiz. Pastdagi tugmani bosing va yukingizni 24/7 rejimda bepul tarqating!",
        parse_mode="HTML",
        reply_markup=markup
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
