import sqlite3

# データベースファイルのパス
db_file_path = "muscle_data.db"

# テーブル名
table_name = "muscle_training"

# SQLiteデータベースの接続
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# テーブル作成SQL
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        日付 DATE NOT NULL,
        種目 TEXT NOT NULL,
        重量 REAL NOT NULL,
        回数 INTEGER NOT NULL,
        セット数 INTEGER NOT NULL,
        コメント TEXT
    )
""")

# コミットして接続を閉じる
conn.commit()
conn.close()

print(f"{db_file_path} が作成されました。テーブル '{table_name}' も作成されました。")
