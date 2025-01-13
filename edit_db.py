import sqlite3

# データベースに接続
conn = sqlite3.connect("training_data.db")
cursor = conn.cursor()

# 更新クエリを実行
cursor.execute("""
UPDATE training
SET home_training = 'OK'
WHERE date = '2025-01-13' AND core_training = 'OK' AND 
      peripheral_vision = 'NG' AND indoor_handling = 'NG' AND 
      stretching = 'NG' AND running = 0.0 AND home_training = 'NG'
""")

# 保存して接続を閉じる
conn.commit()
conn.close()

print("2行目のhome_trainingをOKに更新しました。")
