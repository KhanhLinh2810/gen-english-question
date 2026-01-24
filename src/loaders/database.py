import json
import os
from datetime import datetime
from sqlalchemy import Text, DateTime, JSON, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Import config từ file env của bạn
from env import config

# 1. Cấu hình Database URL
database_url = f"mysql+asyncmy://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['database']}"
# 2. Khởi tạo Engine
engine = create_async_engine(
    database_url,
    pool_size=config['db'].get('pool_size', 8),
    max_overflow=config['db'].get('max_overflow', 32),
    pool_recycle=config['db'].get('pool_recycle', 3600), 
    pool_pre_ping=True,  # QUAN TRỌNG: Kiểm tra kết nối còn sống không trước khi dùng
    connect_args={
        "connect_timeout": 60,
        "ssl": False
    },
    echo=False,
    future=True,
)

# 3. Khởi tạo Session factory
SessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# 4. Định nghĩa Base và Model
class Base(DeclarativeBase):
    pass

class AIQuestion(Base):
    __tablename__ = "ai_questions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text)  
    type: Mapped[str] = mapped_column(String(50)) 
    
    # [{"content": "...", "explaination": "...", "is_correct": true}, ...]
    choices: Mapped[list] = mapped_column(JSON) 
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Generator cung cấp session cho các thao tác database"""
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()

async def save_questions_to_db(list_questions: list, db: AsyncSession):
    """Hàm hỗ trợ lưu nhanh danh sách câu hỏi"""
    new_objs = [AIQuestion(content=str(q)) for q in list_questions]
    db.add_all(new_objs)
    await db.flush()
    return len(new_objs)

async def save_questions_task(final_data: list):
    """Hàm này sẽ chạy ngầm sau khi user đã nhận được phản hồi"""
    async with SessionLocal() as db:
        try:
            for item in final_data:
                new_db_question = AIQuestion(
                    content=json.dumps(item, ensure_ascii=False)
                )
                db.add(new_db_question)
            await db.commit()
        except Exception as e:
            await db.rollback()