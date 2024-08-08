from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
key_info = KeyboardButton(text="Информация")
key_count = KeyboardButton(text="Рассчитать")
key_buy = KeyboardButton(text="Купить")
kb.add(
    key_info,
    key_count,
    key_buy,
)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
key_calc_calories = InlineKeyboardButton(
    text="Рассчитать норму калорий", callback_data="key_calc_calories"
)
key_get_formula = InlineKeyboardButton(
    text="Формулы расчёта", callback_data="key_get_formulas"
)
inline_kb.add(key_calc_calories, key_get_formula)

inline_buy_kb = InlineKeyboardMarkup(resize_keyboard=True)
key_product_1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
key_product_2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
key_product_3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
key_product_4 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
inline_buy_kb.add(
    key_product_1,
    key_product_2,
    key_product_3,
    key_product_4,
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start_command(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=inline_kb)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f"{i}.jpeg", "rb") as photo:
            await message.answer_photo(
                photo,
                f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}",
            )
    await message.answer("Выберите продукт для покупки::", reply_markup=inline_buy_kb)


@dp.callback_query_handler(text="product_buying")
async def get_formulas(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text="key_get_formulas")
async def send_confirm_message(call):
    await call.message.answer("10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(г) + 5")
    await call.answer()


@dp.callback_query_handler(text="key_calc_calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        result = (
            10 * int(data["weight"])
            + 6.25 * int(data["growth"])
            - 5 * int(data["age"])
            + 5
        )
        await message.answer(f"Ваша норма калорий: {result}")
    except ValueError:
        await message.answer("Возраст Рост и Вес должны быть числами")
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)