from sqlalchemy.orm import (relationship,mapped_column,
                            Mapped,Session,DeclarativeBase)
from sqlalchemy import Integer,String,ForeignKey
from  sqlalchemy.ext.asyncio import (create_async_engine,AsyncSession,
                                     AsyncAttrs,async_sessionmaker)
from config import MYSQL_URL


engine = create_async_engine(MYSQL_URL ,echo=True)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase,AsyncAttrs):
    pass

# Создали таблицу категорию
class Category(Base):
    __tablename__ = 'category'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(50))
    
    games = relationship('Game', back_populates="category")


# Создали таблицу игры
class Game(Base):
    __tablename__ = 'game'

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(50))
    description:Mapped[str] = mapped_column(String(250))
    image:Mapped[str] = mapped_column(String(250))
    key: Mapped[str]  = mapped_column(String(250))
    price: Mapped[int] = mapped_column(Integer())
    count: Mapped[int] = mapped_column(Integer())
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    
    category = relationship('Category',back_populates="games")
    
    
    
# Создание таблиц с использованием ассинхронности 
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Добавление категории
# async def add_category():
#     async with async_session() as session:
        
# #         category = Game(name='minecraft',
# #                         description = ''' Игра крутая очень динамичная , мне нравится''' ,
# # image = '/home/hasan/Desktop/game-key/database/image/mine.jpg',
# #                         category_id = ,
# #                         )
        
#         session.add(category)
#         await session.commit()
#         await session.refresh(category)
#         return category



# from random import randint
# songs = ['Mirbek Atabekov', 'Lady Gaga', 'Bill Eilish' , 'BTS',
#          'Moldanazar', 'Gorillaz', 'Imagine Dragons', 
#          'Dead blonde' 'Zemphir', '91', 'Beatls']

# random_num = randint(len(songs))
# print(songs[random_num])