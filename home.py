import streamlit as st
import pandas as pd
import sqlite3

from database import init_db, insert_data, get_data, update_data

st.write("Hello world")
st.write("test")

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


# 初期化
init_db()

# タイトル
st.title("SQLite Database Example with Streamlit")

# メニュー選択
menu = st.sidebar.selectbox("Menu", ["View Data", "Add Data", "Update Data"])

# データ表示
if menu == "View Data":
    st.subheader("View Data")
    data = get_data()
    if data:
        for row in data:
            st.write(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
    else:
        st.write("No data available.")

# データ追加
elif menu == "Add Data":
    st.subheader("Add Data")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    if st.button("Add"):
        insert_data(name, age)
        st.success(f"Data added: {name}, {age}")

# データ更新
elif menu == "Update Data":
    st.subheader("Update Data")
    data = get_data()
    if data:
        user_id = st.selectbox("Select User ID", [row[0] for row in data])
        name = st.text_input("New Name")
        age = st.number_input("New Age", min_value=1, step=1)
        if st.button("Update"):
            update_data(user_id, name, age)
            st.success(f"Data updated for ID {user_id}: {name}, {age}")
    else:
        st.write("No data available to update.")
