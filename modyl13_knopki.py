from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio



api = '6837044561:AAGvbniMV6FhdUcALLQ14zKmq0be1iXgo18'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text = 'Информация')
button2 = KeyboardButton(text = 'Рассчитать')
kb.row(button, button2)




@dp.message_handler(text = 'Информация')
async def inport(message):
    await message.answer('Чтобы рассчитать калории, нажми на кнопку "Рсссчитать')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет', reply_markup = kb)



@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first1 = message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(first2 = message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(first3 = message.text)
    data = await state.get_data()
    calories = 10*int(data['first3'])+6.5*int(data['first2'])-5*int(data['first1'])+5
    await message.answer(f'Ваша норма калорий:{calories}')
    await state.finish()

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Чтобы узнать калории, надо было нажать кнопку "Рассчитать')


@dp.message_handler()
async def start(message):
    await message.answer('Введите команду /start, чтобы начать общение')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)