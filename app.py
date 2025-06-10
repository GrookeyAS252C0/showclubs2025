import streamlit as st
import pandas as pd
import math
from clubs_data import CLUBS_DATA

# ページ設定
st.set_page_config(
    page_title="🌟 部活動一覧 - 日本大学第一中学・高等学校",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# スタイル設定
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700&family=Nunito:wght@300;400;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Noto Sans JP', 'Nunito', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        margin: 1rem;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .super-header {
        text-align: center;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        color: white;
        padding: 2.5rem 1rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .super-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="white" opacity="0.3"/><circle cx="80" cy="30" r="1.5" fill="white" opacity="0.4"/><circle cx="40" cy="70" r="1" fill="white" opacity="0.3"/><circle cx="90" cy="80" r="2.5" fill="white" opacity="0.2"/><circle cx="10" cy="90" r="1.8" fill="white" opacity="0.3"/></svg>');
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .super-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .super-subtitle {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    .fun-filter {
        background: linear-gradient(135deg, #ffeaa7, #fab1a0);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 3px solid #fdcb6e;
    }
    
    .filter-emoji {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .filter-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .club-super-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        border: 3px solid #ddd;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .club-super-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .club-super-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        border-color: #ff6b6b;
    }
    
    .club-super-card:hover::before {
        transform: scaleX(1);
    }
    
    .mega-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .club-super-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 0.8rem;
        line-height: 1.3;
    }
    
    .club-fun-info {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 12px rgba(116, 185, 255, 0.3);
    }
    
    .club-quick-tags {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    
    .fun-tag {
        background: #fd79a8;
        color: white;
        padding: 0.25rem 0.8rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(253, 121, 168, 0.3);
    }
    
    .fun-tag.beginner {
        background: #00b894;
    }
    
    .fun-tag.gender {
        background: #a29bfe;
    }
    
    .detail-super-header {
        background: linear-gradient(135deg, #ff7675, #fd79a8, #6c5ce7);
        background-size: 400% 400%;
        animation: gradientShift 6s ease infinite;
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .detail-super-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .super-info-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 3px solid #ddd;
        position: relative;
        overflow: hidden;
    }
    
    .super-info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);
    }
    
    .super-info-card h3 {
        color: #2d3436;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .rainbow-box {
        background: linear-gradient(135deg, #fff5cd, #ffe8cc);
        border: 2px solid #fdcb6e;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(253, 203, 110, 0.2);
    }
    
    .mega-number {
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 30px rgba(0, 184, 148, 0.3);
        transform: perspective(1000px) rotateX(5deg);
    }
    
    .mega-number-value {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .mega-number-label {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 600;
    }
    
    .fun-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .fun-grid-item {
        background: linear-gradient(135deg, #a8e6cf, #88d8a3);
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(168, 230, 207, 0.3);
        border: 2px solid #6c5ce7;
    }
    
    .fun-grid-label {
        font-weight: 700;
        color: #2d3436;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .fun-grid-value {
        color: #2d3436;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .result-super-count {
        background: linear-gradient(135deg, #fd79a8, #fdcb6e);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(253, 121, 168, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .super-button {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.3);
        margin-bottom: 2rem;
    }
    
    .super-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(108, 92, 231, 0.4);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3) !important;
        border: 3px solid transparent !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
        border-color: #ff7675 !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 15px !important;
        border: 2px solid #ddd !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    
    .achievement-super-box {
        background: linear-gradient(135deg, #ffd93d, #ff6b6b);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 8px 30px rgba(255, 217, 61, 0.3);
    }
    
    .achievement-super-box h3 {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .camp-info-box {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 30px rgba(116, 185, 255, 0.3);
    }
    
    .camp-info-box h3 {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# 部活動のアイコンマッピング
CLUB_ICONS = {
    "硬式野球部": "⚾",
    "マジック・ジャグリング同好会": "🎩",
    "柔道部": "🥋",
    "ダンス部": "💃",
    "女子バスケットボール部": "🏀",
    "軟式野球部": "⚾",
    "水泳部": "🏊",
    "チアリーダー部": "📣",
    "合唱同好会": "🎵",
    "男子バスケットボール部": "🏀",
    "中学野球部": "⚾",
    "アメリカンフットボール": "🏈",
    "バドミントン同好会": "🏸",
    "卓球部": "🏓",
    "数学同好会": "🔢",
    "中学バレーボール部": "🏐",
    "高校バレーボール部": "🏐",
    "物理部": "🔬",
    "写真部": "📷",
    "吹奏楽部": "🎺",
    "ECC": "🌏",
    "テニス部": "🎾",
    "剣道部": "⚔️",
    "陸上部": "🏃",
    "釣り人同好会": "🎣",
    "歴史部": "🏛️",
    "書道部": "✒️"
}

@st.cache_data
def load_data():
    """組み込みデータからDataFrameを作成"""
    df = pd.DataFrame(CLUBS_DATA)
    
    def convert_fullwidth_to_halfwidth(text):
        if pd.isna(text):
            return text
        text = str(text)
        text = text.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
        text = text.replace('名', '').replace('人', '').strip()
        return text
    
    member_columns = [col for col in df.columns if '部員数' in col]
    for col in member_columns:
        df[col] = df[col].apply(convert_fullwidth_to_halfwidth)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    df['総部員数'] = df[member_columns].sum(axis=1)
    return df

def show_club_detail(club_data):
    """部活動の詳細を表示"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 超かっこいいヘッダー
    st.markdown(f"""
    <div class="detail-super-header">
        <div class="detail-super-title">
            {CLUB_ICONS.get(club_data['部活動名を教えてください。'], '🌟')} {club_data['部活動名を教えてください。']}
        </div>
        <div class="super-subtitle">✨ 詳細情報をチェック！ ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 基本情報
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="super-info-card">', unsafe_allow_html=True)
        st.markdown("### 📝 どんな部活？")
        st.markdown(f'<div class="rainbow-box">{club_data["部活紹介をお願いします（最大250文字）。"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="super-info-card">', unsafe_allow_html=True)
        st.markdown("### 📅 いつ・どこで活動？")
        st.markdown('<div class="fun-grid">', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="fun-grid-item">
            <div class="fun-grid-label">🗓️ 活動日</div>
            <div class="fun-grid-value">{club_data['2025年度活動日を教えてください。']}</div>
        </div>
        ''', unsafe_allow_html=True)
        if pd.notna(club_data['2025年度の活動場所を教えてください。']):
            st.markdown(f'''
            <div class="fun-grid-item">
                <div class="fun-grid-label">📍 活動場所</div>
                <div class="fun-grid-value">{club_data['2025年度の活動場所を教えてください。']}</div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="super-info-card">', unsafe_allow_html=True)
        st.markdown("### 💰 入部について")
        st.markdown('<div class="fun-grid">', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="fun-grid-item">
            <div class="fun-grid-label">💵 年間費用</div>
            <div class="fun-grid-value">{club_data['年間費用はどのくらいですか？（合宿費を除いてください）']}</div>
        </div>
        <div class="fun-grid-item">
            <div class="fun-grid-label">👫 性別制限</div>
            <div class="fun-grid-value">{club_data['性別の限定はありますか？']}</div>
        </div>
        <div class="fun-grid-item">
            <div class="fun-grid-label">🌱 初心者</div>
            <div class="fun-grid-value">{'大歓迎！' if club_data['初心者'] == '歓迎' else '要相談'}</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # 総部員数の超目立つ表示
        st.markdown(f"""
        <div class="mega-number">
            <div class="mega-number-value">{int(club_data['総部員数'])}</div>
            <div class="mega-number-label">🎉 総部員数 🎉</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="super-info-card">', unsafe_allow_html=True)
        st.markdown("### 👥 学年別メンバー")
        member_data = {
            '学年': ['中1', '中2', '中3', '高1', '高2', '高3'],
            '女子': [
                int(club_data['2025年06月01日時点の部員数を教えてください（中学・１年・女子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（中学・２年・女子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（中学・３年・女子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（高校・１年・女子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（高校・２年・女子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（高校・３年・女子）。'])
            ],
            '男子': [
                int(club_data['2025年06月01日時点の部員数を教えてください（中学・１年・男子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（中学・２年・男子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（中学・３年・男子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（高校・１年・男子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（高校・２年・男子）。']),
                int(club_data['2025年06月01日時点の部員数を教えてください（高校・３年・男子）。'])
            ]
        }
        member_df = pd.DataFrame(member_data)
        member_df['合計'] = member_df['女子'] + member_df['男子']
        
        st.dataframe(member_df, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="super-info-card">', unsafe_allow_html=True)
        st.markdown("### 👨‍🏫 先生・コーチ")
        st.markdown('<div class="fun-grid">', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="fun-grid-item">
            <div class="fun-grid-label">👨‍🏫 顧問の先生</div>
            <div class="fun-grid-value">{club_data['顧問の先生の人数と性別を教えてください']}</div>
        </div>
        <div class="fun-grid-item">
            <div class="fun-grid-label">🏃‍♂️ コーチ</div>
            <div class="fun-grid-value">{club_data['コーチの人数と性別を教えてください。']}</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 活動実績と合宿情報
    st.markdown('<div class="achievement-super-box">', unsafe_allow_html=True)
    st.markdown("### 🏆 2024年度の成果")
    achievements = club_data["2024度活動実績を教えてください。以下のフォーマットでお願いいたします。\n大会名：順位"]
    st.markdown(f'<div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;">{achievements}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if club_data['合宿はありますか？'] == 'あります':
        st.markdown('<div class="camp-info-box">', unsafe_allow_html=True)
        st.markdown("### 🏕️ 合宿情報")
        if pd.notna(club_data['令和6年度の合宿の詳細を教えてください（場所・期間・費用）。']):
            st.markdown(f'<div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;">{club_data["令和6年度の合宿の詳細を教えてください（場所・期間・費用）。"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;">合宿はありますが、詳細は未定です。</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # データ読み込み
    try:
        df = load_data()
    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {e}")
        return
    
    # セッション状態の初期化
    if 'selected_club' not in st.session_state:
        st.session_state.selected_club = None
    
    # 戻るボタンと詳細表示
    if st.session_state.selected_club is not None:
        if st.button("🔙 一覧に戻る", key="back_button"):
            st.session_state.selected_club = None
            st.rerun()
        
        # 選択された部活の詳細を表示
        club_data = df[df['部活動名を教えてください。'] == st.session_state.selected_club].iloc[0]
        show_club_detail(club_data)
    else:
        # メインコンテナ
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # 超かっこいいヘッダー
        st.markdown("""
        <div class="super-header">
            <div class="super-title">🌟 日本大学第一中学・高等学校</div>
            <div class="super-subtitle">2025年度 部活動ガイド 〜君の青春はここから始まる〜</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 部活動一覧の表示
        # フィルタリングオプション
        st.markdown('<div class="fun-filter">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title"><span class="filter-emoji">🔍</span>君にぴったりの部活を見つけよう！</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            gender_filter = st.selectbox("🚻 性別制限", ["すべて", "制限なし", "女子のみ", "男子のみ"])
        with col2:
            beginner_filter = st.selectbox("🌱 初心者歓迎", ["すべて", "歓迎", "要相談"])
        with col3:
            sort_order = st.selectbox("📊 並び順", ["名前順", "部員数順"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # フィルタリング
        filtered_df = df.copy()
        if gender_filter != "すべて":
            gender_map = {"制限なし": "ありません", "女子のみ": "女子のみ", "男子のみ": "男子のみ"}
            filtered_df = filtered_df[filtered_df['性別の限定はありますか？'] == gender_map[gender_filter]]
        
        if beginner_filter != "すべて":
            if beginner_filter == "歓迎":
                filtered_df = filtered_df[filtered_df['初心者'] == '歓迎']
            else:
                filtered_df = filtered_df[filtered_df['初心者'] != '歓迎']
        
        # ソート
        if sort_order == "部員数順":
            filtered_df = filtered_df.sort_values('総部員数', ascending=False)
        else:
            filtered_df = filtered_df.sort_values('部活動名を教えてください。')
        
        # グリッド表示
        st.markdown(f'<div class="result-super-count">🎯 見つかった部活動: {len(filtered_df)}件</div>', unsafe_allow_html=True)
        
        # 3列のグリッドで表示
        cols_per_row = 3
        rows = math.ceil(len(filtered_df) / cols_per_row)
        
        for row in range(rows):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                idx = row * cols_per_row + col_idx
                if idx < len(filtered_df):
                    club = filtered_df.iloc[idx]
                    club_name = club['部活動名を教えてください。']
                    icon = CLUB_ICONS.get(club_name, '🌟')
                    
                    with cols[col_idx]:
                        # 超かっこいいボタンを作成
                        if st.button(
                            f"{icon}",
                            key=f"club_{idx}",
                            use_container_width=True,
                            help=f"クリックして{club_name}の詳細を見る"
                        ):
                            st.session_state.selected_club = club_name
                            st.rerun()
                        
                        # カスタムカードデザイン
                        st.markdown(f"""
                        <div class="club-super-card">
                            <div class="mega-icon">{icon}</div>
                            <div class="club-super-name">{club_name}</div>
                            <div class="club-fun-info">👥 {int(club['総部員数'])}人の仲間</div>
                            <div class="club-quick-tags">
                                <span class="fun-tag beginner">{'✨ 初心者OK' if club['初心者'] == '歓迎' else '💪 経験者向け'}</span>
                                <span class="fun-tag gender">{club['性別の限定はありますか？']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()