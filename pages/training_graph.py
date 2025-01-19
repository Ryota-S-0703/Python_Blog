import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np  # 目盛りの範囲設定に使用
import matplotlib.dates as mdates  # 日付フォーマット用

# 日本語フォントを設定
import matplotlib.font_manager as fm

# 日本語フォントのパスを取得
font_path = "C:/Windows/Fonts/meiryo.ttc"  # 適切なフォントを指定

# 日本語フォントを設定
jp_font = fm.FontProperties(fname=font_path)
rcParams['font.family'] = jp_font.get_name()

# タイトルを表示
st.title("📊 トレーニングデータのグラフ表示")

# データベースからデータを取得する関数
def get_data_from_db():
    conn = sqlite3.connect("training_data.db")
    query = "SELECT * FROM training"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# データ取得
df = get_data_from_db()

# データを日付順に並べ替える
df['date'] = pd.to_datetime(df['date'])  # 日付列をdatetime型に変換
df = df.sort_values(by='date')

# ランニング距離を数値型に変換
df['running'] = pd.to_numeric(df['running'], errors='coerce')  # 変換失敗時はNaN

# グラフ作成
if not df.empty:
    st.subheader("🏃‍♂️ ランニング距離の推移")
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['running'], marker='o', label='ランニング距離')

    # 縦軸の範囲と目盛り設定
    max_distance = df['running'].max() if not df['running'].isnull().all() else 0
    max_limit = max(10, int(np.ceil(max_distance / 2)) * 2)  # 最大値に応じて10以上で丸める
    plt.yticks(np.arange(0, max_limit + 1, 2))  # 2刻みの目盛り設定

    # 日付ラベルのフォーマット設定
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # 7日間隔でラベルを設定
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 日付フォーマット: 年-月-日
    plt.xticks(rotation=45, fontsize=10)  # ラベルを45度傾けて見やすくする

    plt.title("ランニング距離の推移", fontproperties=jp_font)
    plt.xlabel("日付", fontproperties=jp_font)
    plt.ylabel("距離 (km)", fontproperties=jp_font)
    plt.grid(True)
    plt.legend(prop=jp_font)
    st.pyplot(plt)
else:
    st.write("データがありません。")
