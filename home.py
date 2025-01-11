import streamlit as st
import pandas as pd
import sqlite3

st.write("Hello world")

# データベース接続とテーブル作成
def init_db():
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# データの挿入
def insert_data(name, age):
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

# データの取得
def get_data():
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    return rows

# データの更新
def update_data(user_id, name, age):
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, user_id))
    conn.commit()
    conn.close()