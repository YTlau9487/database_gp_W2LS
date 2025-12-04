from flask import Flask
import os
from sqlalchemy import text
from flask_app import routes
from flask_app.utils.database import engine

# Read the whole file, split by semicolons, and run each statement separately
with open("flask_app/db/library.sql", "r", encoding="utf-8") as f:
    sql_commands = f.read().split(";")  # splits on every ;

with engine.connect() as conn:
    for command in sql_commands:
        cmd = command.strip()
        if cmd:  # skip empty lines
            conn.execute(text(cmd))
    conn.commit()  # very important!

print("All tables created successfully!")

with open("flask_app/db/insertVal.sql", "r", encoding="utf-8") as f:
    sql_commands = f.read().split(";")  # splits on every ;

with engine.connect() as conn:
    for command in sql_commands:
        cmd = command.strip()
        if cmd:  # skip empty lines
            conn.execute(text(cmd))
    conn.commit()  # very important!

print("All records created successfully!")

app = Flask(__name__)
# 设置 secret key，供 Flask session 使用。优先从环境变量读取，默认为开发用的占位字符串。
app.secret_key = os.environ.get("SECRET_KEY", "dev_local_secret_key")
routes.init_routes(app)


