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
        index='日付',
        columns='種目',
        values='セル内容',
        aggfunc=lambda x: ' / '.join(x)  # 同じ種目が1日に複数回ある場合、区切る
    )

    return pivot_table.fillna('')  # NaNを空文字列に変換

# 縦書きHTMLテーブル作成関数
def generate_vertical_html_table(table_data):
    html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: center;
            vertical-align: bottom; /* 下揃え */
        }
        th {
            writing-mode: vertical-rl;
        }
        td {
            background-color: lightgreen;
        }
        td:empty {
            background-color: white;
        }
        td:first-child {
            background-color: white; /* 日付セルを緑にしない */
        }
    </style>
    <table>
        <thead>
            <tr>
                <th>日付</th>
    """
    # ヘッダー部分
    for col in table_data.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    # データ部分（新しい日付順）
    for idx, row in table_data.iterrows():
        html += f"<tr><td>{idx}</td>"
        for cell in row:
            html += f"<td>{cell}</td>" if cell else "<td></td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

# StreamlitのUI
st.title("筋トレデータの管理")

# データ取得
df = fetch_data()

if df.empty:
    st.write("データがありません。筋トレデータを入力してください。")
else:
    # 表データ準備
    table_data = prepare_table_data(df)

    # HTMLテーブル生成
    html_table = generate_vertical_html_table(table_data)

    # 表を表示
    st.markdown(html_table, unsafe_allow_html=True)

# 他のセクションやフォームはそのまま維持
st.subheader("過去の筋トレ履歴")
if not df.empty:
    st.write(df)
else:
    st.write("まだ筋トレのデータがありません。")
