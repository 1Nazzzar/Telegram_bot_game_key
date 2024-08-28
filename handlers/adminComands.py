from database.models import Game
from .keyboards import categories_kb2
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.queryset import *
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID
from handlers.keyboards import categories_kb3

admin_router = Router()


class AddCategory(StatesGroup):
    name = State()


async def check_admin(message: Message) -> bool:
    return message.from_user.id == ADMIN_ID


@admin_router.message(Command('add_category'))
async def add_category(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer('Эта команда только для адмиистратора')
        return
    await message.answer("Введите название категории")
    await state.set_state(AddCategory.name)


@admin_router.message(AddCategory.name)
async def add_name(message: Message, state: FSMContext):
    await add_category_name(message.text)
    await message.answer("Категория добавлена")
    await state.clear()


class AddGame(StatesGroup):
    name = State()
    description = State()
    image = State()
    key = State()
    count = State()
    price = State()
    category_id = State()


async def check_admin(message: Message) -> bool:
    return message.from_user.id == ADMIN_ID


class DeleteCategory(StatesGroup):
    category = State()


 


@admin_router.message(Command('delete_category'))
async def delete_cat(message: Message):
    # if not await check_admin(message):
    #     await message.answer('Эта команда только для администратора')
    #     return

    # Отправляем сообщение с клавиатурой выбора категорий
    await message.answer('Выберите категорию', reply_markup=await categories_kb3())


@admin_router.callback_query(F.data.startswith('category3_'))
async def del_cat(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    await del_cat(category_id)
    await callback.message.answer('Категория удалена')


# @admin_router.callback_query(F.data.startswith())

# @admin_router.callback_query(DeleteCategory.category)
# async def del_category(callback: CallbackQuery):
#     category_id = int(callback.data.split(_)[1])
#     await del_category(category_id)


@admin_router.message(Command('add_game'))
async def add_name(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer('Эта команда только для адмиистратора')
        return
    await message.answer('Введите название игры')
    await state.set_state(AddGame.name)

# @admin_router.message(Command('all_games'))
# async def show_all(message:Message, state:FSMContext):
#      if not await check_admin(message):
#         await message.answer('Эта команда только для адмиистратора')
#         return


@admin_router.message(AddGame.name)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание игры')
    await state.set_state(AddGame.description)


@admin_router.message(AddGame.description)
async def add_image(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Добавьте изображение')
    await state.set_state(AddGame.image)


@admin_router.message(AddGame.image)
async def add_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[0].file_id)
    await message.answer('Введите ключ от игры')
    await state.set_state(AddGame.key)


@admin_router.message(AddGame.key)
async def add_key(message: Message, state: FSMContext):
    await state.update_data(key=message.text)
    await message.answer('Введите количество ключей')
    await state.set_state(AddGame.count)


@admin_router.message(AddGame.count)
async def add_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    await message.answer('Введите цену ключа')
    await state.set_state(AddGame.price)


@admin_router.message(AddGame.price)
async def add_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer('Выберите категорию игры', reply_markup=await categories_kb2())
    await state.set_state(AddGame.category_id)


@admin_router.callback_query(AddGame.category_id)
async def add_category_id(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category_id=callback.data.split('_')[1])
    data = await state.get_data()
    game = Game(
        name=data['name'],
        description=data['description'],
        image=data['image'],
        key=data['key'],
        count=data['count'],
        price=data['price'],
        category_id=data['category_id'],
    )
    await add_game_db(game)
    await callback.message.answer('Игра добавлена')
    await state.clear()
