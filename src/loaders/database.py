from env import config

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

database_url = f"mysql+aiomysql://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['database']}"
engine = create_async_engine(
    database_url,
    pool_size=config['db']['pool_size'],
    max_overflow=0,
    pool_recycle=3600,
    echo=False,
    future=True,
)
SessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()