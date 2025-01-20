import sqlite3
import pandas as pd

conn = sqlite3.connect("training_data.db")
df = pd.read_sql_query("SELECT * FROM training", conn)
print(df)
conn.close()