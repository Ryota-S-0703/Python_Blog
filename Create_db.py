import sqlite3

# データベースファイルを作成・接続
conn = sqlite3.connect("training_data.db")
cursor = conn.cursor()

# テーブルを作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS training (
    date TEXT,
    core_training TEXT,
    peripheral_vision TEXT,
    indoor_handling TEXT,
    stretching TEXT,
    running TEXT,
    home_training TEXT
)
""")

# データを挿入
cursor.execute("""
INSERT INTO training (date, core_training, peripheral_vision, indoor_handling, stretching, running, home_training)
VALUES
('2025/01/11', 'OK', 'OK', 'OK', 'OK', 'OK', 'OK')
""")

# 保存して接続を閉じる
conn.commit()
conn.close()
