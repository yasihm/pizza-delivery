import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# URL para async (troca postgresql:// por postgresql+asyncpg://)
SYNC_DATABASE_URL = os.getenv("DATABASE_URL")
if not SYNC_DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada")

# Converte para async URL
DATABASE_URL = SYNC_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Sessão assíncrona
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependência para obter sessão
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session