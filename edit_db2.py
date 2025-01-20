import pandas as pd
import sqlite3

# CSVファイルのパス
csv_file_path = r"C:\temp\koushin.csv"

# SQLiteデータベースのパス
db_file_path = "training_data.db"

# テーブル名
table_name = "training"

# CSVデータを読み込む
def load_csv(file_path):
    # CSVを読み込み、不要なインデックス列を無視
    df = pd.read_csv(file_path, index_col=0)  # 最初の空の列をインデックスとして無視
    df.rename(columns=lambda x: x.strip(), inplace=True)  # 列名の余分な空白を除去
    df['日付'] = pd.to_datetime(df['日付'])  # 日付列をdatetime型に変換
    return df

# データベースに更新する
def update_database(csv_df, db_path, table_name):
    # データベース接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブルが存在するか確認し、なければ作成
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            "日付" DATE,
            "体幹" TEXT,
            "周辺視野" TEXT,
            "ハンドリング" TEXT,
            "ストレッチ" TEXT,
            "ランニング距離 (km)" REAL,
            "20時までに自宅" TEXT,
            "comment" TEXT
        )
    """)

    # テーブルの内容を置き換え
    csv_df.to_sql(table_name, conn, if_exists='replace', index=False)

    # 変更を保存して接続を閉じる
    conn.commit()
    conn.close()

# 実行
try:
    # CSVデータをロード
    csv_data = load_csv(csv_file_path)

    # データベースを更新
    update_database(csv_data, db_file_path, table_name)
    print("データベースを更新しました。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
