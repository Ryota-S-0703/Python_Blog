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

# データベースに新しいデータを追加する関数
def add_data_to_db(date, core, peripheral, indoor, stretch, running, home):
    conn = sqlite3.connect("training_data.db")
    cursor = conn.cursor()
    query = """
    INSERT INTO training (date, core_training, peripheral_vision, indoor_handling, stretching, running, home_training)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (date, core, peripheral, indoor, stretch, running, home))
    conn.commit()
    conn.close()

# データを取得
df = get_data_from_db()

# データを表示
st.subheader("トレーニングデータ")
st.dataframe(df)

st.write("各項目について実施したものをチェックしてください。")

# データ入力
min_date = datetime.date(1900, 1, 1)  # 選択可能な最小日付
max_date = datetime.date(2100, 12, 31)  # 選択可能な最大日付
default_date = datetime.date.today()  # 今日の日付をデフォルトに設定
d = st.date_input('トレーニング実施日', default_date, min_value=min_date, max_value=max_date)

# チェックボックスの作成（デフォルトはオフ）
core_training = "OK" if st.checkbox("体幹トレーニング") else "NG"
peripheral_vision = "OK" if st.checkbox("周辺視野トレーニング") else "NG"
indoor_handling = "OK" if st.checkbox("室内ハンドリング") else "NG"
stretching = "OK" if st.checkbox("ストレッチ") else "NG"
running_distance = st.number_input("ランニング距離（km）", min_value=0.0, step=0.1, value=0.0)
home_training = "OK" if st.checkbox("自宅(20時まで家にいたか)") else "NG"

# データを更新
if st.button(label='データを更新する'):
    # データベースに新しいデータを追加
    add_data_to_db(d, core_training, peripheral_vision, indoor_handling, stretching, running_distance, home_training)
    st.success("データベースに新しいデータを追加しました！")
    # 最新データを再取得して表示
    df = get_data_from_db()
    st.dataframe(df)