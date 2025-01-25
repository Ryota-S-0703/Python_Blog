import pandas as pd
import sqlite3

# CSVファイルのパス
csv_file_path = r"C:\temp\koushin_muscle.csv"

# SQLiteデータベースのパス
db_file_path = "muscle_data.db"

# テーブル名
table_name = "muscle_training"

# CSVデータを読み込む
def load_csv(file_path):
    df = pd.read_csv(file_path)
    df.rename(columns=lambda x: x.strip(), inplace=True)  # 列名の余分な空白を除去
    df['日付'] = pd.to_datetime(df['日付']).dt.strftime('%Y-%m-%d')  # 日付列を文字列に変換
    return df

# データベースを更新する関数
def update_database(csv_df, db_path, table_name):
    # データベース接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # CSVのデータを一行ずつ処理
    for _, row in csv_df.iterrows():
        # 既存のデータがあるか確認
        cursor.execute(f"""
            SELECT COUNT(*) FROM {table_name}
            WHERE 日付 = ? AND 種目 = ?
        """, (row['日付'], row['種目']))
        result = cursor.fetchone()

        if result[0] > 0:
            # 既存データがある場合、UPDATE
            cursor.execute(f"""
                UPDATE {table_name}
                SET 重量 = ?, 回数 = ?, セット数 = ?, コメント = ?
                WHERE 日付 = ? AND 種目 = ?
            """, (
                row['重量'], row['回数'], row['セット数'], row.get('コメント', ''),
                row['日付'], row['種目']
            ))
        else:
            # 新規データの場合、INSERT
            cursor.execute(f"""
                INSERT INTO {table_name} (日付, 種目, 重量, 回数, セット数, コメント)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row['日付'], row['種目'], row['重量'], row['回数'], row['セット数'], row.get('コメント', '')
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
