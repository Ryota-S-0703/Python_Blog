import streamlit as st
import pandas as pd
import sqlite3
import datetime

# タイトルを表示
st.title("トレーニングデータ管理アプリ")

# データベースからデータを取得する関数
def get_data_from_db():
    conn = sqlite3.connect("training_data.db")
    query = "SELECT * FROM training"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# データを取得
df = get_data_from_db()

# データを表示
st.subheader("トレーニングデータ")
st.dataframe(df)

# データ入力
min_date = datetime.date(1900, 1, 1)
max_date = datetime.date(2100, 12, 31)
d = st.date_input('誕生日を入力してください。', datetime.date(2025, 1, 11), min_value=min_date, max_value=max_date)
