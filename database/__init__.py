from sqlalchemy import MetaData, update, delete, and_, text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.state import InstanceState

from dotenv import load_dotenv
from os import getenv
from inspect import stack
import os
from utils.jwt_token import password_hash

load_dotenv()

PROTOCOL = getenv('DB_CONNECTION')
DRIVER = getenv('DB_DRIVER')
USERNAME = getenv('DB_USERNAME')
PASSWORD = getenv('DB_PASSWORD')
HOST = getenv('DB_HOST')
DB = getenv('DB_DATABASE')


def create_session(database: str):
    db_url = f'{PROTOCOL}+aiomysql://{USERNAME}:{PASSWORD}@{HOST}/{database}'
    engine = create_async_engine(db_url, pool_pre_ping = True, echo = False)

    return sessionmaker(engine, expire_on_commit = False, class_ = AsyncSession)


sessions = {
    'central': create_session(DB),
    'tenant': None
}


metadata = {
    'central': MetaData(),
    'tenant': MetaData()
}


def tenancy_initialize(database: str):
    sessions['tenant'] = create_session(database)


def tenancy_end():
    sessions['tenant'] = None


def configure_metadata():
    caller_frame = stack()[1]
    folder_path = os.path.dirname(caller_frame.filename)
    folder_name = os.path.basename(folder_path)
    # print(folder_name)
    return metadata[folder_name]

def _select_session(cls):
    folder_name = cls.__module__.split('.')[1].lower()

    if folder_name == 'central': sessions['tenant'] = None
    session = sessions[folder_name]

    if session: return session
    raise Exception('Tenant não inicializado')


class Base(DeclarativeBase):
    def dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


    def __repr__(self):
        attributes = ', '.join(f'{k} = {v}' for k, v in vars(self).items() if not isinstance(v, InstanceState))
        return f'{self.__class__.__name__}({attributes})'


    @classmethod
    async def update(cls, id: int, **kwargs):
        AioSession = _select_session(cls)

        async with AioSession() as db:
            stmt = update(cls).where(getattr(cls, 'id') == id).values(**kwargs)
            result = await db.execute(stmt)
            await db.commit()
            
            if result.rowcount != 0:
                data = await cls.find_one(id = id)
                return data
    

    @classmethod
    async def delete(cls, **kwargs):
        AioSession = _select_session(cls)

        async with AioSession() as db:
            stmt = delete(cls).where(and_(*[getattr(cls, col) == value for col, value in kwargs.items()]))
            result = await db.execute(stmt)
            await db.commit()
            return result.rowcount != 0


    @classmethod
    async def find_one(cls, options = None, **kwargs):
        AioSession = _select_session(cls)

        async with AioSession() as db:
            stmt = select(cls).filter_by(**kwargs)

            if options: stmt = stmt.options(options)

            result = await db.execute(stmt)
            return result.scalars().first()


    @classmethod
    async def find_many(cls, options = None, **kwargs):
        AioSession = _select_session(cls)

        async with AioSession() as db:
            stmt = select(cls).filter_by(**kwargs)

            if options:
                stmt = stmt.options(options)
            
            result = await db.execute(stmt)
            return result.scalars().all()
        

    @classmethod    
    async def find_many_regex(cls, **kwargs):
        AioSession = _select_session(cls)

        async with AioSession() as db:
            col, re = list(kwargs.items())[0]
            
            stmt = select(cls).filter(text(f'{col} REGEXP "{re}"'))
            result = await db.execute(stmt)
            return result.scalars().all()
    

    @classmethod
    async def find_or_new(cls, options = None, **kwargs):
        find = await cls.find_one(options, **kwargs)
        if find: return find

        AioSession = _select_session(cls)

        async with AioSession() as db:
            query = cls(**kwargs)
            db.add(query)
            await db.commit()
            await db.refresh(query)

        return query


    @classmethod
    async def create(cls, **kwargs):
        AioSession = _select_session(cls)

        async with AioSession() as db:
            query = cls(**kwargs)
            db.add(query)
            await db.commit()
            await db.refresh(query)

        return query


    # @classmethod
    # def configure_metadata(cls):
    #     folder_name = cls.__module__.split('.')[1].lower()
    #     cls.metadata = metadata.get(folder_name)