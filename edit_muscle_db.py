import sqlite3

# SQLiteデータベースファイル
db_file_path = "muscle_data.db"
table_name = "muscle_training"

# 特定のIDを削除する関数
def delete_rows_by_id(ids):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    
    # 複数のIDを削除するためのSQL文
    query = f"DELETE FROM {table_name} WHERE id IN ({','.join(['?']*len(ids))})"
    cursor.execute(query, ids)
    
    conn.commit()
    conn.close()

# ID 9と10を削除
delete_rows_by_id([11])

print("ID 11の行が削除されました。")
