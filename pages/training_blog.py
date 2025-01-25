import streamlit as st
import pandas as pd
import sqlite3

# タイトルを表示
st.title("🏋️‍♀️ トレーニングブログ")

# カスタムCSSを使ってセクション分けラインの色を変更
st.markdown("""
    <style>
        hr {
            border: 0;
            border-top: 3px solid #FF6347;  /* 色を変更 */
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# データベースからトレーニングデータを取得する関数
def get_training_data():
    conn = sqlite3.connect("training_data.db")
    query = "SELECT * FROM training"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# データベースから筋トレデータを取得する関数
def get_muscle_data():
    conn = sqlite3.connect("muscle_data.db")
    query = "SELECT 日付, 種目, 重量, 回数, セット数, コメント FROM muscle_training"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# トレーニングデータと筋トレデータを取得
training_df = get_training_data()
muscle_df = get_muscle_data()

# 日付列をdatetime型に変換
training_df['date'] = pd.to_datetime(training_df['date'])
muscle_df['日付'] = pd.to_datetime(muscle_df['日付'])

# トレーニングデータを新しい順にソート
training_df = training_df.sort_values(by='date', ascending=False)

# カレンダーで日付を選択
selected_date = st.date_input("日付を選択", training_df['date'].max())  # 最新日付を初期値に
formatted_date = selected_date.strftime('%Y-%m-%d')

# 選択された日付に対応するデータをフィルタリング
filtered_training = training_df[training_df['date'] == pd.to_datetime(selected_date)]
filtered_muscle = muscle_df[muscle_df['日付'] == pd.to_datetime(selected_date)]

# トレーニング内容の表示
if not filtered_training.empty:
    st.subheader(f"{formatted_date}")
    
    # トレーニング内容の表
    st.write("**トレーニング内容**")
    training_data = filtered_training.drop(columns=['date', 'comment'])
    st.table(training_data)
    
    # トレーニングコメントの表示
    st.subheader("コメント")
    st.write(f"**{filtered_training['comment'].iloc[0]}**")
    
    # 筋トレ内容の表示
    if not filtered_muscle.empty:
        st.write("**その日にやった筋トレ内容**")
        muscle_data = filtered_muscle.drop(columns=['日付', 'コメント'])
        st.table(muscle_data)
        
        # 筋トレごとのコメント
        st.subheader("筋トレメニュータイトル")
        for _, row in filtered_muscle.iterrows():
            if pd.notna(row['コメント']):
                st.write(f"**{row['種目']}**")
                st.write(row['コメント'])
else:
    st.write("選択した日付のデータはありません。")

# セクション分けライン
st.markdown('<hr style="border-top: 3px solid #FF6347;">', unsafe_allow_html=True)

# すべてのデータを新しい順で一覧表示
st.subheader("すべてのトレーニング内容とコメント")

# 過去データの一覧表示
for date in training_df['date'].dt.strftime('%Y-%m-%d').unique():
    # トレーニングデータをフィルタリング
    day_training = training_df[training_df['date'].dt.strftime('%Y-%m-%d') == date]
    day_muscle = muscle_df[muscle_df['日付'].dt.strftime('%Y-%m-%d') == date]
    
    st.subheader(f"{date}")
    
    # トレーニング内容の表
    st.write("**トレーニング内容**")
    training_data = day_training.drop(columns=['date', 'comment'])
    st.table(training_data)
    
    # トレーニングコメントの表示
    st.subheader("コメント")
    st.write(f"**{day_training['comment'].iloc[0]}**")
    
    # 筋トレ内容の表示
    if not day_muscle.empty:
        st.write("**その日にやった筋トレ内容**")
        muscle_data = day_muscle.drop(columns=['日付', 'コメント'])
        st.table(muscle_data)
        
        # 筋トレごとのコメント
        st.subheader("筋トレメニュータイトル")
        for _, row in day_muscle.iterrows():
            if pd.notna(row['コメント']):
                st.write(f"**{row['種目']}**")
                st.write(row['コメント'])
    
    # セクション分けライン
    st.markdown("---")
