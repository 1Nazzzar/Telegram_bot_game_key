from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from database.queryset import *

menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Категории')], [KeyboardButton(text='Все игры')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню',
    one_time_keyboard=True)

# inline_test = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Аркада',callback_data='button1')],
#     [InlineKeyboardButton(text='Шутер',callback_data='button2')],
#     [InlineKeyboardButton(text='Аркада',callback_data='button3')]

# ])


async def categories_kb():
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    for category in categories:
        builder.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f'category_{category.id}'  # == 'category_1'
        ))
    return builder.adjust(2).as_markup()

# object1({'id':1 ,'name':'Шутер'})
# object2({'id':2 ,'name':'RPG'})


async def categories_kb2():
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    for category in categories:
        builder.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f'category2_{category.id}'  # == 'category2_1'
        ))
    return builder.adjust(2).as_markup()


async def categories_kb3():
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    for category in categories:
        builder.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f'category3_{category.id}'  # == 'category2_1'
        ))
    return builder.adjust(2).as_markup()

PAGE_SIZE = 2


async def games_kb(category_id, page):
    offset = (page - 1) * PAGE_SIZE
    builder = InlineKeyboardBuilder()
    all_games = await get_games(category_id, offset=offset, limit=PAGE_SIZE)
    for game in all_games:
        builder.add(InlineKeyboardButton(
            text=game.name,
            callback_data=f'game_{game.id}'
        ))
    if page > 1:
        builder.add(InlineKeyboardButton(
            text='<<',
            callback_data=f'page_{category_id}_{page-1}'
        ))
    if len(all_games) == PAGE_SIZE:
        builder.add(InlineKeyboardButton(
            text='>>',
            callback_data=f'page_{category_id}_{page+1}'
        ))

    return builder.adjust(2).as_markup()


async def all_games_kb(page):
    offset = (page - 1) * PAGE_SIZE
    builder = InlineKeyboardBuilder()
    games = await get_all_games(offset=offset, limit=PAGE_SIZE)
    for game in games:
        builder.add(InlineKeyboardButton(
            text=game.name,
            callback_data=f'allgame_{game.id}'
        ))
    if page > 1:
        builder.add(InlineKeyboardButton(
            text='<<',
            callback_data=f'allpage_{page-1}'
        ))
    if len(games) == PAGE_SIZE:
        builder.add(InlineKeyboardButton(
            text='>>',
            callback_data=f'allpage_{page+1}'
        ))

    return builder.adjust(2).as_markup()
 

async def game_delete_kb(game_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Удалить',
        callback_data=f'delete_{game_id}'  # == 'delete_1'
    ))
    return builder.adjust(1).as_markup()



async def back_to_categories_kb(game_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Назад к категориям',
        callback_data='back_to_categories'
    ))
    builder.add(InlineKeyboardButton(
        text='купить игру',
        callback_data='buy_game_{game_id}'
    ))
    builder.add(InlineKeyboardButton(
        text='Удалить',
        callback_data=f'delete_{game_id}'  # == 'delete_1'
    ))
    return builder.adjust(1).as_markup()
