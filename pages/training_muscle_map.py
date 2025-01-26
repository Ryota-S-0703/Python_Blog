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

# 表データを作成する関数
def prepare_table_data(df):
    # 日付列をdatetime型に変換し、時間部分を除去
    df['日付'] = pd.to_datetime(df['日付']).dt.date
    df = df.sort_values(by='日付', ascending=False)  # 新しい順にソート

    # 種目ごとのセル内容を作成
    df['セル内容'] = df[['重量', '回数', 'セット数']].astype(str).agg('-'.join, axis=1)

    # ピボットテーブル作成
    pivot_table = df.pivot_table(
        index='種目',
        columns='日付',
        values='セル内容',
        aggfunc=lambda x: ' / '.join(x)  # 同じ日付に同じ種目が複数回ある場合、区切る
    )

    return pivot_table.fillna('')  # NaNを空文字列に変換

# StreamlitのUI
st.title("筋トレデータの管理")

# データ取得
df = fetch_data()

if df.empty:
    st.write("データがありません。筋トレデータを入力してください。")
else:
    # 表データ準備
    table_data = prepare_table_data(df)

    # 日付列を左から最新順に並び替え
    table_data = table_data[sorted(table_data.columns, reverse=True)]

    # 表の表示
    st.subheader("筋トレ履歴表")

    # データフレームのスタイリング
    def highlight_cells(val):
        """セルが空でなければ緑色で背景を塗る"""
        return 'background-color: lightgreen;' if val else ''

    styled_table = table_data.style.applymap(highlight_cells)
    st.dataframe(styled_table, use_container_width=True)

# 他のセクションやフォームはそのまま維持
st.subheader("過去の筋トレ履歴")
if not df.empty:
    st.write(df)
else:
    st.write("まだ筋トレのデータがありません。")
