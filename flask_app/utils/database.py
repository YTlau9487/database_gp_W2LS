# utils/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('user')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port', 3306)}/{os.getenv('database')}"

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
