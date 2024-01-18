
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


# Database configuration
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "sample_user",
    "password": "StrongPassword123!",
    "database": "sample_db",
}

engine = create_async_engine("mysql+aiomysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % db_config, echo=True)
Base = declarative_base()

# Create an asynchronous session
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

