import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

API_TOKEN = '8664981128:AAHT_yb1NU_fPiyZsedD84TGDhrPUNWfR5n0'
ADMIN_ID = 6887494552  # встав свій Telegram ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ---------- ГОЛОВНЕ МЕНЮ ----------
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏨 Номери", callback_data="view_rooms")],
        [InlineKeyboardButton(text="📷 Галерея", callback_data="gallery")],
        [InlineKeyboardButton(text="💰 Ціни", callback_data="prices")],
        [InlineKeyboardButton(text="📅 Забронювати", callback_data="booking")],
        [InlineKeyboardButton(text="📞 Контакти", callback_data="contacts")]
    ])

# ---------- МЕНЮ НОМЕРІВ ----------
def get_rooms_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Люкс", callback_data="room_lux")],
        [InlineKeyboardButton(text="🛏 Стандарт", callback_data="room_std")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])

# ---------- START ----------
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🌲 *Forrest Hotel — Східниця*\n\n"
        "Відпочинок серед карпатського лісу\n\n"
        "Оберіть розділ:",
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )

# ---------- НОМЕРИ ----------
@dp.callback_query(F.data == "view_rooms")
async def show_rooms(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🏨 Оберіть номер:",
        reply_markup=get_rooms_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "room_lux")
async def room_lux_info(callback: types.CallbackQuery):
    await callback.message.answer_photo(
        photo="https://images.unsplash.com/photo-1566073771259-6a8506099945",
        caption="💎 *Люкс*\n\n"
                "• Панорамний вид\n"
                "• Сніданок включено\n"
                "• Велике ліжко\n\n"
                "💰 2500 грн/доба",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_rooms_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "room_std")
async def room_std_info(callback: types.CallbackQuery):
    await callback.message.answer_photo(
        photo="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85",
        caption="🛏 *Стандарт*\n\n"
                "• Затишний номер\n"
                "• Wi-Fi\n"
                "• Душ\n\n"
                "💰 900 грн/доба",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_rooms_menu()
    )
    await callback.answer()

# ---------- ГАЛЕРЕЯ ----------
@dp.callback_query(F.data == "gallery")
async def gallery(callback: types.CallbackQuery):
    await callback.message.answer_photo(
        photo="https://images.unsplash.com/photo-1501117716987-c8e1ecb210e1",
        caption="📷 Фото готелю"
    )
    await callback.answer()

# ---------- ЦІНИ ----------
@dp.callback_query(F.data == "prices")
async def prices(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💰 *Ціни*\n\n"
        "Стандарт — 900 грн\n"
        "Люкс — 2500 грн",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu()
    )
    await callback.answer()

# ---------- КОНТАКТИ ----------
@dp.callback_query(F.data == "contacts")
async def contacts(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📞 Контакти\n\n"
        "📍 Східниця\n"
        "📱 +380XXXXXXXXX\n\n"
        "Напишіть нам у Telegram 👇",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# ---------- БРОНЮВАННЯ ----------
@dp.callback_query(F.data == "booking")
async def booking(callback: types.CallbackQuery):
    await callback.message.answer(
        "📅 Напишіть:\n\n"
        "• дату заїзду\n"
        "• дату виїзду\n"
        "• кількість гостей"
    )
    await callback.answer()

# ---------- ПЕРЕСИЛКА АДМІНУ ----------
@dp.message()
async def forward_to_admin(message: types.Message):
    await bot.send_message(
        ADMIN_ID,
        f"📩 Нова заявка:\n\n{message.text}"
    )
    await message.answer("✅ Дякуємо! Ми скоро з вами зв'яжемось.")

# ---------- НАЗАД ----------
@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Головне меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# ---------- СТАРТ ----------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(e)