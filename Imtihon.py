import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from buttons import KursTanlash, Kursga_yozilish, Kurslar, Menu, TelefonRaqam

bot = Bot(token = "8776058956:AAFnyGSkyqIx7NQ46D2gPRcgF4bdxm-BI-E")
dp = Dispatcher()

class RegistrationStates(StatesGroup):
    full_name = State()
    phone = State()
    course = State()

COURSES = {
    "python": {"name": "Python", "price": "500$", "duration": "3 oy"},
    "web": {"name": "Web dasturlash", "price": "400$", "duration": "6 oy"},
    "frontend": {"name": "Frontend", "price": "300$", "duration": "4 oy"},
    "design": {"name": "Grafik dizayn", "price": "200$", "duration": "2 oy"},
}

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    full_name = message.from_user.full_name
    await message.answer(f"Xush kelibsiz, {full_name}! Kerakli bo'limni tanlang:",
                            reply_markup = await Menu())

@dp.message(F.text == "Kurslar")
async def reaction_to_kurslar(message: Message):
    await message.answer("Kurslardan birini tanlang:",
                            reply_markup = await Kurslar())

@dp.message(F.text == "Kursga yozilish")
async def begin_registration(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(RegistrationStates.full_name)
    await message.answer("Ism va familiyangizni kiriting:",
                            reply_markup = await Kursga_yozilish())

@dp.message(F.text == "Bekor qilish")
async def cancel_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Kursga yozilish bekor qilindi.",
                            reply_markup = await Menu())

@dp.callback_query(F.data == "cancel_registration")
async def cancel_registration_by_button(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("Kursga yozilish bekor qilindi")
    await callback.bot.send_message(
        chat_id = callback.from_user.id,
        text = "Kursga yozilish bekor qilindi.",
        reply_markup = await Menu())

@dp.message(RegistrationStates.full_name)
async def receive_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await state.set_state(RegistrationStates.phone)
    await message.answer("Telefon raqamingizni kiriting:",
                            reply_markup = await TelefonRaqam())

@dp.message(RegistrationStates.phone)
async def receive_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone.strip())
    await state.set_state(RegistrationStates.course)
    await message.answer("Kursni tanlang:",
                            reply_markup = await KursTanlash())

@dp.callback_query(RegistrationStates.course, F.data.in_(COURSES))
async def receive_course(callback: CallbackQuery, state: FSMContext):
    course_key = callback.data or ""
    course = COURSES.get(course_key)
    await state.update_data(course = course["name"])
    user_data = await state.get_data()
    await state.clear()
    await callback.answer("Kurs tanlandi")
    await callback.bot.send_message(
        chat_id = callback.from_user.id,
        text = (
            "Kursga yozilish ma'lumotlari:\n"
            f"Ism-familiya: {user_data['full_name']}\n"
            f"Telefon raqam: {user_data['phone']}\n"
            f"Kurs: {user_data['course']}"
        ), reply_markup = await Menu())

@dp.callback_query(F.data.in_(COURSES))
async def show_course_info(callback: CallbackQuery):
    course = COURSES.get(callback.data or "")
    await callback.answer()
    await callback.bot.send_message(
        chat_id = callback.from_user.id,
        text = (
            f"Kurs: {course['name']}\n"
            f"Davomiyligi: {course['duration']}\n"
            f"Narxi: {course['price']}"
        ))

@dp.message(F.text == "Markaz haqida")
async def show_center_info(message: Message):
    await message.answer(" Markazimizga gap yo'q",
                            reply_markup = await Menu())

@dp.message(F.text == "Aloqa")
async def show_contact_info(message: Message):
    await message.answer(
        "Aloqa ma'lumotlari:\n"
        "Telefon: +998 90 123 45 67\n"
        "Manzil: Sayilgoh 001-A\n"
        "Ish vaqti: Dushanba–Juma, 10:00–12:00",
        reply_markup = await Menu())

async def main():
    await dp.start_polling(bot)

asyncio.run(main())