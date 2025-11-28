import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('user')}:{(os.getenv('password'))}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database')}",
    echo=True
)

Session = sessionmaker(bind=engine)
