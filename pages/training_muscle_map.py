import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

# データをヒートマップ用に整形する関数
def prepare_heatmap_data(df):
    # 日付列をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付']).dt.date
    df = df.sort_values(by='日付', ascending=False)  # 新しい順にソート

    # ピボットテーブル作成
    pivot_table = df.pivot_table(
        index='日付',
        columns='種目',
        values='換算値',
        aggfunc=np.sum
    )

    # 各種目ごとに標準化（0~1スケール）
    normalized = pivot_table.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)
    return normalized.fillna(0)  # NaNを0で埋める

# StreamlitのUI
st.title("筋トレデータの管理")

# データ取得
df = fetch_data()

if df.empty:
    st.write("データがありません。筋トレデータを入力してください。")
else:
    # ヒートマップ用データ準備
    heatmap_data = prepare_heatmap_data(df)

    # ヒートマップの描画
    st.subheader("種目別負荷ヒートマップ")

    # 図の設定
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        heatmap_data,
        cmap="Reds",
        linewidths=0.5,
        linecolor="gray",
        cbar_kws={'label': '負荷（正規化）'},
        xticklabels=True,
        yticklabels=True
    )

    # 横軸ラベルを縦書きに
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel("種目", fontsize=12)
    plt.ylabel("日付", fontsize=12)
    plt.title("筋トレ種目別負荷ヒートマップ", fontsize=14)

    # Streamlitに表示
    st.pyplot(plt)

# 他のセクションやフォームはそのまま維持
st.subheader("過去の筋トレ履歴")
if not df.empty:
    st.write(df)
else:
    st.write("まだ筋トレのデータがありません。")
