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
            "running_distance": float(running) if running else 0.0,  # 型変換を追加
            "home_training": True if home == "OK" else False,
        }
    else:
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

# 今日のデータを取得する関数
def get_today_data(df):
    today = datetime.date.today()
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df[df['date'] == today]

# データを取得
df = get_data_from_db()

# 今日のデータを抽出
today_data = get_today_data(df)

# 今日の進捗度を計算
if not today_data.empty:
    # 判定用列
    check_columns = ['core_training', 'peripheral_vision', 'indoor_handling', 'stretching', 'running', 'home_training']

    # 今日の最初のデータを基に計算
    row = today_data.iloc[0]
    achieved_count = sum(
        1 for col in check_columns 
        if row[col] == 'OK' or (col == 'running' and pd.to_numeric(row[col], errors='coerce') > 0.0)
    )
    total_count = len(check_columns)

    # 進捗率を大きく表示
    st.subheader("🎯 今日のトレーニング進捗")
    progress_percentage = (achieved_count / total_count) * 100
    st.metric(label="進捗率", value=f"{achieved_count} / {total_count} 項目達成", delta=f"{progress_percentage:.1f}%")
else:
    st.write("今日のデータはまだありません。")

# 日付列でソート（最新順）
df['date'] = pd.to_datetime(df['date'])  # 日付列をdatetime型に変換
df = df.sort_values(by='date', ascending=False)  # 最新順に並べ替え

# running列を数値型に変換して小数点以下1桁に丸める
df['running'] = pd.to_numeric(df['running'], errors='coerce').round(1)

# 日付列を "YYYY-MM-DD" の形式に変換
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# 列名を日本語にマッピング
columns_mapping = {
    'date': '日付',
    'core_training': '体幹',
    'peripheral_vision': '周辺視野',
    'indoor_handling': 'ハンドリング',
    'stretching': 'ストレッチ',
    'running': 'ランニング距離 (km)',
    'home_training': '20時までに自宅'
}
df.rename(columns=columns_mapping, inplace=True)

# NGや0.0の部分に赤色をつけるための関数
def highlight_ng(val):
    # 型に応じて条件を分岐
    if isinstance(val, (int, float)) and val == 0.0:
        return 'background-color: red'  # 距離が0.0の場合
    elif isinstance(val, str) and val == "NG":
        return 'background-color: red'  # "NG"の場合
    else:
        return ''  # 条件に合わない場合はスタイルなし

# NGや0.0の部分に赤色をつけるためのスタイル適用
styled_df = df.style \
    .format({'ランニング距離 (km)': '{:.1f}'}) \
    .applymap(highlight_ng, subset=list(columns_mapping.values())[1:])  # マッピング後の列名で適用

# データフレームを表示
st.subheader("📋 トレーニングデータ一覧")
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
    
    # 日付に基づいてデフォルト値を取得
    defaults = get_defaults_for_date(d)

    # チェックボックスの作成（デフォルト値を使用）
    col1, col2, col3 = st.columns(3)
    with col1:
        core_training = "OK" if st.checkbox("体幹トレーニング", value=defaults["core_training"]) else "NG"
        indoor_handling = "OK" if st.checkbox("室内ハンドリング", value=defaults["indoor_handling"]) else "NG"
    with col2:
        peripheral_vision = "OK" if st.checkbox("周辺視野トレーニング", value=defaults["peripheral_vision"]) else "NG"
        stretching = "OK" if st.checkbox("ストレッチ", value=defaults["stretching"]) else "NG"
    with col3:
        running_distance = st.number_input(
        "ランニング距離（km）",
        min_value=0.0,
        step=0.1,
        value=float(defaults["running_distance"])  # 型変換を追加
        )
        home_training = "OK" if st.checkbox("自宅(20時まで家にいたか)", value=defaults["home_training"]) else "NG"

    # 送信ボタン
    submit_button = st.form_submit_button(label="💾 データを更新する")

# データベース更新とフィードバック
if submit_button:
    update_or_add_data(d, core_training, peripheral_vision, indoor_handling, stretching, running_distance, home_training)
    st.success("✅ データベースを更新しました！")
    # 最新データを再取得して表示
    df = get_data_from_db()

    # 日付列でソート（最新順）
    df['date'] = pd.to_datetime(df['date'])  # 日付列をdatetime型に変換
    df = df.sort_values(by='date', ascending=False)  # 最新順に並べ替え

    # running列を数値型に変換して小数点以下1桁に丸める
    df['running'] = pd.to_numeric(df['running'], errors='coerce').round(1)

    # 日付列を "YYYY-MM-DD" の形式に変換
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    # 列名を日本語にマッピング
    columns_mapping = {
        'date': '日付',
        'core_training': '体幹',
        'peripheral_vision': '周辺視野',
        'indoor_handling': 'ハンドリング',
        'stretching': 'ストレッチ',
        'running': 'ランニング距離 (km)',
        'home_training': '20時までに自宅'
    }
    df.rename(columns=columns_mapping, inplace=True)

    # NGや0.0の部分に赤色をつけるためのスタイル適用
    styled_df = df.style \
        .format({'ランニング距離 (km)': '{:.1f}'}) \
        .applymap(highlight_ng, subset=list(columns_mapping.values())[1:])  # マッピング後の列名で適用

    st.dataframe(styled_df)
else:
    st.write("送信ボタンがまだ押されていません。")
    
st.markdown("---")  # セクション分け用ライン

# フッター
st.write("🔗 [Streamlit公式ドキュメント](https://docs.streamlit.io/)を参考にカスタマイズしてください。")
