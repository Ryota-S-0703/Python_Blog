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
min_date = datetime.date(1900, 1, 1)  # 選択可能な最小日付
max_date = datetime.date(2100, 12, 31)  # 選択可能な最大日付
default_date = datetime.date.today()  # 今日の日付をデフォルトに設定
d = st.date_input('トレーニング実施日', default_date, min_value=min_date, max_value=max_date)
