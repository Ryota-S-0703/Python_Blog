import streamlit as st
import pandas as pd
import sqlite3

# タイトルを表示
st.title("🏋️‍♀️ トレーニングブログ")

# データベースからデータを取得する関数
def get_data_from_db():
    conn = sqlite3.connect("training_data.db")
    query = "SELECT * FROM training"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# データ取得
df = get_data_from_db()
df['date'] = pd.to_datetime(df['date'])  # 日付をdatetime型に変換

# 新しい順にソート
df = df.sort_values(by='date', ascending=False)  # 新しい順に並べ替え

# カレンダー表示で日付を選択
selected_date = st.date_input("日付を選択", df['date'].max())  # 最新日付を初期値に

# 日付の表示形式を変更
formatted_date = selected_date.strftime('%Y-%m-%d')  # 「2025-01-19」の形式で表示

# 選択した日付に対応するデータを取得
filtered_df = df[df['date'] == pd.to_datetime(selected_date)]

# 日付をフォーマット
filtered_df['date'] = filtered_df['date'].dt.strftime('%Y-%m-%d')

# トレーニング内容とコメントの表示
if not filtered_df.empty:
    # トレーニング内容（コメントなし）
    st.subheader(f"日付: {formatted_date}")
    st.write("**トレーニング内容**")
    
    # コメントはテーブルに含まない
    training_data = filtered_df.drop(columns=['date', 'comment'])
    st.table(training_data)
    
    # コメントの表示
    st.subheader("コメント")
    st.write(f"**{filtered_df['comment'].iloc[0]}**")
else:
    st.write("選択した日付のデータはありません。")

# セクション分けライン
st.markdown("---")  # これ以降にすべてのトレーニング内容とコメントを表示

# すべてのデータを新しい順に表示
st.subheader("すべてのトレーニング内容とコメント")

# 新しい順で日付ごとに表示
for date in df['date'].dt.strftime('%Y-%m-%d').unique():
    # その日のデータを取得
    day_data = df[df['date'].dt.strftime('%Y-%m-%d') == date]
    
    # トレーニング内容（コメントなし）
    st.subheader(f"日付: {date}")
    st.write("**トレーニング内容**")
    training_data = day_data.drop(columns=['date', 'comment'])
    st.table(training_data)
    
    # コメントの表示
    st.subheader("コメント")
    st.write(f"**{day_data['comment'].iloc[0]}**")
    
    # セクション分けライン
    st.markdown("---")
