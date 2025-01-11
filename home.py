import streamlit as st
import pandas as pd
import sqlite3
import datetime

# タイトルを表示
st.title("🏋️ トレーニングデータ管理アプリ")

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

# データベースに新しいデータを追加する関数
def add_data_to_db(date, core, peripheral, indoor, stretch, running, home):
    conn = sqlite3.connect("training_data.db")
    cursor = conn.cursor()
    query = """
    INSERT INTO training (date, core_training, peripheral_vision, indoor_handling, stretching, running, home_training)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (date, core, peripheral, indoor, stretch, running, home))
    conn.commit()
    conn.close()

# データを取得
df = get_data_from_db()

# レイアウト: 表の表示エリア
st.subheader("📋 トレーニングデータ一覧")
st.dataframe(
    df,
    width=800,  # 横幅の指定
    height=300  # 表の高さを調整
)

st.markdown("---")  # セクション分け用ライン

# レイアウト: 入力フォーム
st.subheader("📝 新しいデータの追加")
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
    add_data_to_db(d, core_training, peripheral_vision, indoor_handling, stretching, running_distance, home_training)
    st.success("✅ データベースに新しいデータを追加しました！")
    # 最新データを再取得して表示
    df = get_data_from_db()
    st.dataframe(df)

st.markdown("---")  # セクション分け用ライン

# フッター
st.write("🔗 [Streamlit公式ドキュメント](https://docs.streamlit.io/)を参考にカスタマイズしてください。")
