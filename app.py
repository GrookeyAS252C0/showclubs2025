import streamlit as st
import pandas as pd
import math
from clubs_data import CLUBS_DATA

# ページ設定
st.set_page_config(
    page_title="部活動一覧 - 日本大学第一中学・高等学校",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# スタイル設定
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e8ecf0;
    }
    
    .club-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .club-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #e8ecf0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        position: relative;
        overflow: hidden;
    }
    
    .club-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .club-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        border-color: #667eea;
    }
    
    .club-card:hover::before {
        transform: scaleX(1);
    }
    
    .club-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    .club-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .club-members {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 500;
    }
    
    .detail-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .detail-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #e8ecf0;
    }
    
    .info-card h3 {
        color: #2d3748;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .back-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .back-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .achievement-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #fbbf24;
        margin: 1rem 0;
    }
    
    .filter-container {
        display: flex;
        gap: 1rem;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .result-count {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        margin: 1rem 0;
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
    # 組み込みデータからDataFrameを作成
    df = pd.DataFrame(CLUBS_DATA)
    
    # 全角数字を半角数字に変換する関数
    def convert_fullwidth_to_halfwidth(text):
        if pd.isna(text):
            return text
        text = str(text)
        # 全角数字を半角数字に変換
        text = text.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
        # 「名」「人」などの単位を削除
        text = text.replace('名', '').replace('人', '').strip()
        return text
    
    # 部員数列を数値に変換
    member_columns = [col for col in df.columns if '部員数' in col]
    for col in member_columns:
        # 全角数字を半角数字に変換してから数値化
        df[col] = df[col].apply(convert_fullwidth_to_halfwidth)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # 総部員数を計算
    df['総部員数'] = df[member_columns].sum(axis=1)
    
    return df

def show_club_detail(club_data):
    """部活動の詳細を表示"""
    # ヘッダー部分
    st.markdown(f"""
    <div class="detail-header">
        <div class="detail-title">
            {CLUB_ICONS.get(club_data['部活動名を教えてください。'], '🏫')} {club_data['部活動名を教えてください。']}
        </div>
        <div class="main-subtitle">部活動詳細情報</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 基本情報
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📝 部活紹介")
        st.info(club_data['部活紹介をお願いします（最大250文字）。'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📅 活動情報")
        st.write(f"**活動日**: {club_data['2025年度活動日を教えてください。']}")
        if pd.notna(club_data['2025年度の活動場所を教えてください。']):
            st.write(f"**活動場所**: {club_data['2025年度の活動場所を教えてください。']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 💰 費用・その他")
        st.write(f"**年間費用**: {club_data['年間費用はどのくらいですか？（合宿費を除いてください）']}")
        st.write(f"**性別制限**: {club_data['性別の限定はありますか？']}")
        st.write(f"**初心者**: {'歓迎' if club_data['初心者'] == '歓迎' else '要相談'}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 👥 部員数")
        # 部員数テーブル作成
        member_data = {
            '学年': ['中学1年', '中学2年', '中学3年', '高校1年', '高校2年', '高校3年'],
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
        
        st.dataframe(member_df, hide_index=True)
        
        # メトリック表示を更新
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(club_data['総部員数'])}</div>
            <div class="metric-label">総部員数</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 👨‍🏫 指導体制")
        st.write(f"**顧問**: {club_data['顧問の先生の人数と性別を教えてください']}")
        st.write(f"**コーチ**: {club_data['コーチの人数と性別を教えてください。']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 活動実績と合宿情報
    st.markdown('<div class="achievement-section">', unsafe_allow_html=True)
    st.markdown("### 🏆 2024年度活動実績")
    st.text(club_data['2024度活動実績を教えてください。以下のフォーマットでお願いいたします。\n大会名：順位'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if club_data['合宿はありますか？'] == 'あります':
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🏕️ 合宿情報")
        if pd.notna(club_data['令和6年度の合宿の詳細を教えてください（場所・期間・費用）。']):
            st.info(club_data['令和6年度の合宿の詳細を教えてください（場所・期間・費用）。'])
        else:
            st.info("合宿はありますが、詳細は未定です。")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # メインヘッダー
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🏫 日本大学第一中学・高等学校</div>
        <div class="main-subtitle">2025年度部活動データベース</div>
    </div>
    """, unsafe_allow_html=True)
    
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
        if st.button("← 一覧に戻る", key="back_button"):
            st.session_state.selected_club = None
            st.rerun()
        
        # 選択された部活の詳細を表示
        club_data = df[df['部活動名を教えてください。'] == st.session_state.selected_club].iloc[0]
        show_club_detail(club_data)
    else:
        # 部活動一覧の表示
        # フィルタリングオプション
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown("### 🔍 検索・フィルター")
        col1, col2, col3 = st.columns(3)
        with col1:
            gender_filter = st.selectbox("性別制限", ["すべて", "制限なし", "女子のみ", "男子のみ"])
        with col2:
            beginner_filter = st.selectbox("初心者", ["すべて", "歓迎", "要相談"])
        with col3:
            sort_order = st.selectbox("並び順", ["名前順", "部員数順"])
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
        st.markdown(f'<div class="result-count">該当する部活動: {len(filtered_df)}件</div>', unsafe_allow_html=True)
        
        # 3列のグリッドで表示（より見やすく）
        cols_per_row = 3
        rows = math.ceil(len(filtered_df) / cols_per_row)
        
        for row in range(rows):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                idx = row * cols_per_row + col_idx
                if idx < len(filtered_df):
                    club = filtered_df.iloc[idx]
                    club_name = club['部活動名を教えてください。']
                    icon = CLUB_ICONS.get(club_name, '🏫')
                    
                    with cols[col_idx]:
                        # カスタムカードデザインでボタンを作成
                        if st.button(
                            f"{icon}",
                            key=f"club_{idx}",
                            use_container_width=True,
                            help=f"{club_name} - {int(club['総部員数'])}人"
                        ):
                            st.session_state.selected_club = club_name
                            st.rerun()
                        
                        # ボタンの下に情報を表示
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: -10px;">
                            <div class="club-name">{club_name}</div>
                            <div class="club-members">👥 {int(club['総部員数'])}人</div>
                        </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()