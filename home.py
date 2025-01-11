import streamlit as st
import pandas as pd
import sqlite3

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