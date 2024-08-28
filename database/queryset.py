from .models import *

from sqlalchemy import select,delete,update

async def get_categories():
    async with async_session() as session:
       result = await session.scalars(select(Category))
       return result

async def get_games(category_id,offset,limit):
    async with async_session() as session:
       result = await session.scalars(select(Game).where(
           Game.category_id == category_id).offset(offset).limit(limit))
       
       return result.all()
async def get_all_games(offset,limit):
    async with async_session() as session:
        result = await session.scalars(select(Game).offset(offset).limit(limit))
    
    return result.all()

async def get_game(game_id):
    async with async_session() as session:
       result = await session.scalar(select(Game).where(
           Game.id == game_id))
       return result

async def add_category_name(category_name):
    async with async_session() as session:
        category = Category(name=category_name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
    
async def add_game_db(game):
    async with async_session() as session:
        
        session.add(game)
        await session.commit()
        await session.refresh(game)
        return game


async def delete_category(category_id):
    async with async_session() as session:
        await session.execute(delete(Category).where(Category.id == category_id))
        await session.commit()


async def delete_game(game_id):
    async with async_session() as session:
        await session.execute(delete(Game).where(Game.id == game_id))
        await session.commit()

