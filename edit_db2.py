import sqlite3

# データベースファイルを接続
conn = sqlite3.connect("training_data.db")
cursor = conn.cursor()

# 新しいカラムを追加
try:
    cursor.execute("ALTER TABLE training ADD COLUMN comment TEXT")
    print("カラム 'comment' を追加しました。")
except sqlite3.OperationalError as e:
    print(f"カラム追加エラー: {e}")

# テスト用: 新しいカラムにデータを挿入（必要なら）
cursor.execute("""
UPDATE training
SET comment = '初期コメント'
WHERE date = '2025/01/11'
""")

# 保存して接続を閉じる
conn.commit()
conn.close()
