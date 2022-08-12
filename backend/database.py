from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from models import Base, category, product, order 

db_url = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(
    db_url,
    echo=True,
)

session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# session for tg bot
def get_session_no_gen() -> AsyncSession:
    session = session_maker()
    return session

# session for fastapi
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_maker()
    yield session
    await session.close()

async def create_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Here I'm adding categories to db 'cause functionality of the app doesn't imply adding categories from the app
    async with get_session_no_gen() as session:
        categories = [
            {
                "id": 22,
                "name": "Shampoo",
            },
            {
                "id": 21,
                "name": "Health products",
            },
            {
                "id": 2,
                "name": "Accessories",
            },
            {
                "id": 1,
                "name": "Uncategorized",
            },
        ]
        try:
            session.add_all([category.Category(**c) for c in categories])
            await session.commit()
        except:
            pass

