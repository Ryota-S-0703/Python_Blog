#換算値というカラムの追加
import sqlite3

# データベースファイルのパス
db_file_path = "muscle_data.db"
table_name = "muscle_training"

# SQLiteデータベースの接続
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# 換算値カラムを追加するSQL文
cursor.execute(f"""
    ALTER TABLE {table_name}
    ADD COLUMN 換算値 REAL
""")

# コミットして接続を閉じる
conn.commit()
conn.close()

print(f"'{table_name}' テーブルに '換算値' カラムが追加されました。")

