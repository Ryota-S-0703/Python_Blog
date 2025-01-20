#Stremlit Cloud上のDBのデータをCSVに落として来て、現在のデータベースに更新する
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
    df = pd.read_csv(file_path)
    df.rename(columns=lambda x: x.strip(), inplace=True)  # 列名の余分な空白を除去
    df['日付'] = pd.to_datetime(df['日付']).dt.strftime('%Y-%m-%d')  # 日付列を文字列に変換
    return df

# データベースに更新する
def update_database(csv_df, db_path, table_name):
    # データベース接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # CSVのデータを一行ずつ処理
    for _, row in csv_df.iterrows():
        # 既存のデータがあるか確認
        cursor.execute(f"""
            SELECT COUNT(*) FROM {table_name} WHERE date = ?
        """, (row['日付'],))
        result = cursor.fetchone()

        if result[0] > 0:
            # 既存データがある場合、UPDATE
            cursor.execute(f"""
                UPDATE {table_name}
                SET core_training = ?, peripheral_vision = ?, indoor_handling = ?, 
                    stretching = ?, running = ?, home_training = ?, comment = ?
                WHERE date = ?
            """, (
                row['体幹'], row['周辺視野'], row['ハンドリング'], 
                row['ストレッチ'], row['ランニング距離 (km)'], row['20時までに自宅'], row['comment'], row['日付']
            ))
        else:
            # 新規データの場合、INSERT
            cursor.execute(f"""
                INSERT INTO {table_name} (date, core_training, peripheral_vision, indoor_handling, 
                    stretching, running, home_training, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['日付'], row['体幹'], row['周辺視野'], row['ハンドリング'], 
                row['ストレッチ'], row['ランニング距離 (km)'], row['20時までに自宅'], row['comment']
            ))

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
