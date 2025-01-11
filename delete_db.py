import sqlite3

# データベースファイルに接続
conn = sqlite3.connect("training_data.db")
cursor = conn.cursor()

# テーブル内の全データを削除
cursor.execute("DELETE FROM training")

# 変更を保存
conn.commit()

# テーブルが空か確認（オプション）
cursor.execute("SELECT * FROM training")
data = cursor.fetchall()
print("データベースの状態:", data)  # データが空なら []

# 接続を閉じる
conn.close()
