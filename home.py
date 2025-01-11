import streamlit as st
import pandas as pd
import sqlite3
import datetime

# タイトルを表示
st.title("🏋️ トレーニングデータ管理")

# サイドバー
st.sidebar.title("メニュー")
st.sidebar.write("以下の機能を使ってデータを管理してください。")
st.sidebar.markdown("""
- トレーニングデータの表示
- 新しいデータの追加
- データベースの更新
""")

# データベースからデータを取得する関数
def get_data_from_db():
    conn = sqlite3.connect("training_data.db")
    query = "SELECT * FROM training"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 指定した日付のデフォルト値を取得する関数
def get_defaults_for_date(date):
    conn = sqlite3.connect("training_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM training WHERE date = ?", (date,))
    existing_data = cursor.fetchone()
    conn.close()
    
    if existing_data:
        _, core, peripheral, indoor, stretch, running, home = existing_data
        defaults = {
            "core_training": True if core == "OK" else False,
            "peripheral_vision": True if peripheral == "OK" else False,
            "indoor_handling": True if indoor == "OK" else False,
            "stretching": True if stretch == "OK" else False,
            "running_distance": running,
            "home_training": True if home == "OK" else False,
        }
    else:
        # データが存在しない場合のデフォルト値
        defaults = {
            "core_training": False,
            "peripheral_vision": False,
            "indoor_handling": False,
            "stretching": False,
            "running_distance": 0.0,
            "home_training": False,
        }
    return defaults


# データベースにデータを更新・追加する関数
def update_or_add_data(date, core, peripheral, indoor, stretch, running, home):
    conn = sqlite3.connect("training_data.db")
    cursor = conn.cursor()
    
    # 既存の日付を検索
    cursor.execute("SELECT * FROM training WHERE date = ?", (date,))
    existing_data = cursor.fetchone()
    
    if existing_data:
        # データが存在する場合、更新
        query = """
        UPDATE training
        SET core_training = ?, peripheral_vision = ?, indoor_handling = ?, 
            stretching = ?, running = ?, home_training = ?
        WHERE date = ?
        """
        cursor.execute(query, (core, peripheral, indoor, stretch, running, home, date))
    else:
        # データが存在しない場合、新規追加
        query = """
        INSERT INTO training (date, core_training, peripheral_vision, indoor_handling, stretching, running, home_training)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (date, core, peripheral, indoor, stretch, running, home))
    
    conn.commit()
    conn.close()

# データを取得
df = get_data_from_db()

# NGや0の部分に赤色をつけるための関数
def highlight_ng(val):
    color = 'background-color: red' if val == "NG" or val == 0 else ''
    return color

# レイアウト: 表の表示エリア
st.subheader("📋 トレーニングデータ一覧")
styled_df = df.style.applymap(highlight_ng, subset=['core_training', 'peripheral_vision', 'indoor_handling', 'stretching', 'running', 'home_training'])
st.dataframe(styled_df, width=800, height=300)

st.markdown("---")  # セクション分け用ライン

# レイアウト: 入力フォーム
st.subheader("📝 新しいデータの追加または更新")
with st.form(key="training_form"):
    # データ入力
    min_date = datetime.date(1900, 1, 1)
    max_date = datetime.date(2100, 12, 31)
    default_date = datetime.date.today()
    d = st.date_input('トレーニング実施日', default_date, min_value=min_date, max_value=max_date)

    # チェックボックスの作成（デフォルトはオフ）
    col1, col2, col3 = st.columns(3)
    with col1:
        core_training = "OK" if st.checkbox("体幹トレーニング") else "NG"
        indoor_handling = "OK" if st.checkbox("室内ハンドリング") else "NG"
    with col2:
        peripheral_vision = "OK" if st.checkbox("周辺視野トレーニング") else "NG"
        stretching = "OK" if st.checkbox("ストレッチ") else "NG"
    with col3:
        running_distance = st.number_input("ランニング距離（km）", min_value=0.0, step=0.1, value=0.0)
        home_training = "OK" if st.checkbox("自宅(20時まで家にいたか)") else "NG"

    # 送信ボタン
    submit_button = st.form_submit_button(label="💾 データを更新する")

# データベース更新とフィードバック
if submit_button:
    update_or_add_data(d, core_training, peripheral_vision, indoor_handling, stretching, running_distance, home_training)
    st.success("✅ データベースを更新しました！")
    # 最新データを再取得して表示
    df = get_data_from_db()
    styled_df = df.style.applymap(highlight_ng, subset=['core_training', 'peripheral_vision', 'indoor_handling', 'stretching', 'running', 'home_training'])
    st.dataframe(styled_df)

st.markdown("---")  # セクション分け用ライン

# フッター
st.write("🔗 [Streamlit公式ドキュメント](https://docs.streamlit.io/)を参考にカスタマイズしてください。")
