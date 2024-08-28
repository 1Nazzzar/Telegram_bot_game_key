from aiogram import Router,F
from aiogram.filters import Command,CommandStart
from aiogram.types import Message, CallbackQuery,FSInputFile
from .keyboards import * 

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer(f"""Привет {message.from_user.id}, 
    я бот продавец ключей для игр \n чем могу помочь?""",reply_markup=menu_kb)


# @router.message(F.text.lower() == 'привет')
# async def hello(message: Message):
#     await message.answer('Привет, как дела?')

# @router.message(F.text.startswith('пока'))
# async def byebye(message: Message):
#     await message.answer('До свидания ')

@router.message(F.text == 'Категории') 
async def categories(message: Message): 
    await message.answer('Выберите категорию:',reply_markup= await categories_kb()) 

@router.message(F.text == 'Все игры') 
async def games(message: Message): 
    await message.answer('Выберите игру:', reply_markup= await all_games_kb(page=1))


# @router.message(Command("help"))
# async def help(message: Message):
#     await message.answer('<h1> dice </h1> hello')
from .adminComands import check_admin

@router.callback_query(F.data == 'back_to_categories')
async def back_to_categories(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите категорию:', 
    reply_markup= await categories_kb())

@router.callback_query(F.data.startswith('delete_'))
async def del_game(callback: CallbackQuery):
    
    game_id = callback.data.split('_')[1]
    await delete_game(game_id)
    await callback.message.answer('Игра удалена')

@router.callback_query(F.data.startswith('category_'))
async def category_game(callback: CallbackQuery):
    await callback.message.delete()
    category_id = callback.data.split('_')[1]
    await callback.message.answer('Игры по этой категории: ',
        reply_markup=await games_kb(category_id,page=1))
 
@router.callback_query(F.data.startswith('page_'))
async def game_paginate(callback: CallbackQuery):
    # await callback.message.delete()
    data = callback.data.split('_')
    category_id = data[1]
    page = int(data[2])
    await callback.message.edit_reply_markup(
        reply_markup= await games_kb(category_id,page)
    )
@router.callback_query(F.data.startswith('allpage_'))
async def all_game_paginate(callback: CallbackQuery):
    data = callback.data.split('_')
    page = int(data[1])
    await callback.message.edit_reply_markup(
        reply_markup=await all_games_kb(page)
    )

from database.queryset import get_game

@router.callback_query(F.data.startswith('game_'))
async def game(callback: CallbackQuery):
    await callback.message.delete()
    game_id = callback.data.split('_')[1]
    game = await get_game(game_id)
    if game.image.startswith('http') or game.image.startswith('AgAC'):
        image = game.image
    else:
        image = FSInputFile(game.image)
    await callback.message.answer_photo(photo=image,caption=f'{game.name} \n {game.description}',
          reply_markup= await back_to_categories_kb(game_id))

 
# Напишите кнопку для покупки в детальной информации о игре
# В кнопке должно находиться колличество ключей (50) и сумма в $
# Кнопка находиться под описанием к игре
from payments import create_payment

@router.callback_query(F.data.startswith('buy_game_'))
async def buy_game(callback:CallbackQuery):
    game_id = callback.data.split('_')[2]
    game = await get_game(game_id)

    payment = create_payment(game.price, f'Покупка игры {game.name}')
