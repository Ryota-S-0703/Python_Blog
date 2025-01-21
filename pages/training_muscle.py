import streamlit as st
import sqlite3
import pandas as pd

# SQLiteデータベースファイル
db_file_path = "muscle_data.db"
table_name = "muscle_training"

# データベースからデータを取得する関数
def fetch_data():
    conn = sqlite3.connect(db_file_path)
    query = f"SELECT * FROM {table_name} ORDER BY 日付 DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 今日の日付の筋トレデータを取得する関数
def fetch_today_data(date):
    conn = sqlite3.connect(db_file_path)
    query = f"SELECT * FROM {table_name} WHERE 日付 = ?"
    df = pd.read_sql(query, conn, params=(date,))
    conn.close()
    return df

# 種目ごとの過去最高記録を取得する関数
def fetch_best_records():
    conn = sqlite3.connect(db_file_path)
    exercises = [
        "マルチヒップ", "レッグプレス", "ラットプルダウン", "ロータリートーソ", 
        "スクワット", "デッドリフト", "スタンディングダンベルカール", "オーバーヘッドダンベルトライセプスエクステンション"
    ]
    best_records = []
    
    for exercise in exercises:
        query = f"""
            SELECT 種目, 重量, 回数, セット数, 換算値, 日付
            FROM {table_name}
            WHERE 種目 = ? 
            ORDER BY 換算値 DESC
            LIMIT 1
        """
        df = pd.read_sql(query, conn, params=(exercise,))
        if not df.empty:
            best_records.append(df.iloc[0])  # 最も換算値が高いレコードを追加
    
    conn.close()
    
    # 結果をDataFrameに変換して返す
    return pd.DataFrame(best_records)

# データベースに筋トレデータを追加または更新する関数
def upsert_data(date, exercise, weight, reps, sets, comment):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # 換算値の計算
    converted_value = weight * reps * sets

    # 同じ日付と種目のデータが存在するかを確認
    cursor.execute(f"""
        SELECT id FROM {table_name} WHERE 日付 = ? AND 種目 = ?
    """, (date, exercise))
    
    existing_data = cursor.fetchone()
    
    if existing_data:
        # 既存のデータがある場合、UPDATE
        cursor.execute(f"""
            UPDATE {table_name} 
            SET 重量 = ?, 回数 = ?, セット数 = ?, コメント = ?, 換算値 = ? 
            WHERE id = ?
        """, (weight, reps, sets, comment, converted_value, existing_data[0]))
    else:
        # データが存在しない場合、INSERT
        cursor.execute(f"""
            INSERT INTO {table_name} (日付, 種目, 重量, 回数, セット数, コメント, 換算値)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (date, exercise, weight, reps, sets, comment, converted_value))
    
    conn.commit()
    conn.close()

# StreamlitのUI
st.title("筋トレデータの管理")

# 1. 過去の最高記録の表示
st.subheader("過去の最高記録")
best_records_df = fetch_best_records()

if not best_records_df.empty:
    st.write(best_records_df)
else:
    st.write("最高記録のデータがありません。")

# 2. 今日の筋トレ内容の一覧表示
st.subheader("過去の筋トレ履歴")
df = fetch_data()
if not df.empty:
    st.write(df)
else:
    st.write("まだ筋トレのデータがありません。")

# 3. 新しい筋トレデータを入力するフォーム
st.subheader("新しい筋トレを追加")
date = st.date_input("日付", value=pd.to_datetime('today'))

# 今日の日付のデータがある場合、その内容をデフォルトで表示
today_data = fetch_today_data(date)

# 4. 筋トレ種目の入力フォーム
exercises = [
    "マルチヒップ", "レッグプレス", "ラットプルダウン", "ロータリートーソ", 
    "スクワット", "デッドリフト", "スタンディングダンベルカール", "オーバーヘッドダンベルトライセプスエクステンション"
]

data = []

for exercise in exercises:
    st.write(f"□ {exercise}")
    selected = st.checkbox(f"{exercise} を追加", key=exercise)
    
    # 今日のデータがあればデフォルトで入力
    if selected:
        # 今日のデータに既に存在する場合、デフォルトで表示
        weight_default = 0.0
        reps_default = 1
        sets_default = 1
        comment_default = ""
        
        if not today_data.empty and exercise in today_data['種目'].values:
            exercise_data = today_data[today_data['種目'] == exercise].iloc[0]
            weight_default = exercise_data['重量']
            reps_default = exercise_data['回数']
            sets_default = exercise_data['セット数']
            comment_default = exercise_data['コメント']
        
        weight = st.number_input(f"{exercise}の重量 (kg)", min_value=0.0, value=weight_default, step=0.5)
        reps = st.number_input(f"{exercise}の回数", min_value=1, value=reps_default)
        sets = st.number_input(f"{exercise}のセット数", min_value=1, value=sets_default)
        comment = st.text_area(f"{exercise}のコメント", value=comment_default)
        
        data.append((exercise, weight, reps, sets, comment))

# フォームの送信ボタン
if st.button("筋トレ内容を追加"):
    for exercise, weight, reps, sets, comment in data:
        upsert_data(date, exercise, weight, reps, sets, comment)
    st.success("筋トレ内容が追加または更新されました！")

    # 最新データを再表示
    df = fetch_data()
    st.write(df)
