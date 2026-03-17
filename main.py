import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Твій токен
API_TOKEN = '8664981128:AAHT_yb1NU_fPiyZseD84TGDhrPUNWfR5n0' 

# Налаштування логів (важливо для сервера)
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота з підтримкою Markdown за замовчуванням
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# --- КЛАВІАТУРИ ---

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🏨 Переглянути номери")],
    [KeyboardButton(text="📅 Забронювати відпочинок")],
    [KeyboardButton(text="📜 Прайс"), KeyboardButton(text="📍 Локація")]
], resize_keyboard=True, input_field_placeholder="Оберіть пункт меню...")

rooms_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🌲 Comfort Suite", callback_data="r1")],
    [InlineKeyboardButton(text="⛰ Forest View", callback_data="r2")],
    [InlineKeyboardButton(text="👑 Presidential Loft", callback_data="r3")]
])

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "✨ *Вітаємо у Forrest Hotel, Східниця!*\n\n"
        "Ми поєднали затишок природи та сервіс преміум-класу.\n"
        "Оберіть розділ меню нижче, щоб розпочати 👇"
    )
    await message.answer(welcome_text, reply_markup=main_kb)

@dp.message(F.text == "🏨 Переглянути номери")
async def show_rooms(message: types.Message):
    await message.answer("✨ *Наші найкращі пропозиції:*", reply_markup=rooms_kb)

@dp.callback_query(F.data == "r1")
async def r1(cb: types.CallbackQuery):
    caption = "🌲 *Comfort Suite*\n\nКласичний затишок. Вид на сосновий ліс, ортопедичне ліжко та власна тераса.\n\n💰 *Ціна:* 1200 грн/доба"
    await cb.message.answer_photo(
        photo="https://images.unsplash.com/photo-1505691938895-1758d7eaa511?q=80&w=1200",
        caption=caption
    )
    await cb.answer()

@dp.callback_query(F.data == "r2")
async def r2(cb: types.CallbackQuery):
    caption = "⛰ *Forest View*\n\nПанорамні вікна на гори. Сучасний дизайн та кавомашина у номері.\n\n💰 *Ціна:* 1800 грн/доба"
    await cb.message.answer_photo(
        photo="https://images.unsplash.com/photo-1590490359683-658d3d23f972?q=80&w=1200",
        caption=caption
    )
    await cb.answer()

@dp.callback_query(F.data == "r3")
async def r3(cb: types.CallbackQuery):
    caption = "👑 *Presidential Loft*\n\nНайкращий номер готелю. Власний камін, простора тераса та джакузі.\n\n💰 *Ціна:* 2600 грн/доба"
    await cb.message.answer_photo(
        photo="https://images.unsplash.com/photo-1591088398332-8a7791972843?q=80&w=1200",
        caption=caption
    )
    await cb.answer()

@dp.message(F.text == "📅 Забронювати відпочинок")
async def ask_contact(message: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 Надіслати номер", request_contact=True)],
        [KeyboardButton(text="⬅️ Назад")]
    ], resize_keyboard=True)
    await message.answer("Для бронювання залиште ваш контакт. Адміністратор зателефонує протягом 5 хвилин:", reply_markup=kb)

@dp.message(F.contact)
async def get_contact(message: types.Message):
    # Тут можна додати відправку заявки адміну в приватні повідомлення
    await message.answer("✅ *Дякуємо! Заявку прийнято.*\nОчікуйте на дзвінок адміністратора ✨", reply_markup=main_kb)
    print(f"НОВА ЗАЯВКА: {message.contact.full_name} | {message.contact.phone_number}")

@dp.message(F.text == "📍 Локація")
async def loc(message: types.Message):
    await message.answer("📍 *Ми знаходимось тут:*")
    await bot.send_location(message.chat.id, 49.2312, 23.3441)

@dp.message(F.text == "📜 Прайс")
async def price(message: types.Message):
    price_list = (
        "📜 *Наш прайс-лист:*\n\n"
        "• Comfort Suite: 1200 грн\n"
        "• Forest View: 1800 грн\n"
        "• Presidential Loft: 2600 грн\n\n"
        "_У вартість включено сніданок та СПА._"
    )
    await message.answer(price_list)

@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    await cmd_start(message)

# Запуск
async def main():
    print("--- БОТ ЗАПУЩЕНИЙ У ХМАРІ ---")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())