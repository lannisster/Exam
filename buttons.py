from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

async def Menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text = "Kurslar"), KeyboardButton(text = "Kursga yozilish")],
            [KeyboardButton(text = "Markaz haqida"), KeyboardButton(text = "Aloqa")]
        ],
        resize_keyboard=True,)

async def Kurslar():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "Python", callback_data = "python")],
            [InlineKeyboardButton(text = "Web dasturlash", callback_data = "web")],
            [InlineKeyboardButton(text = "Frontend", callback_data = "frontend")],
            [InlineKeyboardButton(text = "Grafik dizayn", callback_data = "design")]
        ])

async def Kursga_yozilish() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [[KeyboardButton(text = "Bekor qilish")]],
        resize_keyboard = True,
        message = "Ism-familiyangizni kiriting")

async def TelefonRaqam() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Telefon raqamni yuborish", request_contact = True)],
            [KeyboardButton(text = "Bekor qilish")],
        ], resize_keyboard = True,
        message = "Telefon raqamingizni kiriting")

async def KursTanlash() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text = "Python", callback_data = "python")],
            [InlineKeyboardButton(text = "Web dasturlash", callback_data = "web")],
            [InlineKeyboardButton(text = "Frontend", callback_data = "frontend")],
            [InlineKeyboardButton(text = "Grafik dizayn", callback_data = "design")],
            [InlineKeyboardButton(text = "Bekor qilish", callback_data = "cancel_registration")]
        ])