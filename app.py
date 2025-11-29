import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template

load_dotenv()


engine = create_engine(f'mysql+pymysql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}/{os.getenv("dbname")}',echo=True)
session = sessionmaker(bind=engine)

# Read the whole file, split by semicolons, and run each statement separately
with open('library.sql', 'r', encoding='utf-8') as f:
    sql_commands = f.read().split(';')   # splits on every ;

with engine.connect() as conn:
    for command in sql_commands:
        cmd = command.strip()
        if cmd:  # skip empty lines
            conn.execute(text(cmd))
    conn.commit()  # very important!

print("All tables created successfully!")

with open('insertVal.sql', 'r', encoding='utf-8') as f:
    sql_commands = f.read().split(';')   # splits on every ;

with engine.connect() as conn:
    for command in sql_commands:
        cmd = command.strip()
        if cmd:  # skip empty lines
            conn.execute(text(cmd))
    conn.commit()  # very important!

print("All records created successfully!")
