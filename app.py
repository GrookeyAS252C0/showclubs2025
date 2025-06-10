import streamlit as st
import pandas as pd
import math
from clubs_data import CLUBS_DATA

# ページ設定
st.set_page_config(
    page_title="部活動一覧",
    page_icon="🏫",
    layout="wide"
)

# スタイル設定
st.markdown("""
<style>
    .club-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .club-card:hover {
        background-color: #e0e2e6;
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .club-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    .club-name {
        font-size: 16px;
        font-weight: bold;
        color: #333;
    }
    .detail-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .member-table {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
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
    st.markdown(f"## {CLUB_ICONS.get(club_data['部活動名を教えてください。'], '🏫')} {club_data['部活動名を教えてください。']}")
    
    # 基本情報
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 部活紹介")
        st.info(club_data['部活紹介をお願いします（最大250文字）。'])
        
        st.markdown("### 📅 活動情報")
        st.write(f"**活動日**: {club_data['2025年度活動日を教えてください。']}")
        if pd.notna(club_data['2025年度の活動場所を教えてください。']):
            st.write(f"**活動場所**: {club_data['2025年度の活動場所を教えてください。']}")
        
        st.markdown("### 💰 費用・その他")
        st.write(f"**年間費用**: {club_data['年間費用はどのくらいですか？（合宿費を除いてください）']}")
        st.write(f"**性別制限**: {club_data['性別の限定はありますか？']}")
        st.write(f"**初心者**: {'歓迎' if club_data['初心者'] == '歓迎' else '要相談'}")
    
    with col2:
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
        st.metric("総部員数", f"{int(club_data['総部員数'])}人")
        
        st.markdown("### 👨‍🏫 指導体制")
        st.write(f"**顧問**: {club_data['顧問の先生の人数と性別を教えてください']}")
        st.write(f"**コーチ**: {club_data['コーチの人数と性別を教えてください。']}")
    
    # 活動実績と合宿情報
    st.markdown("### 🏆 2024年度活動実績")
    st.text(club_data['2024度活動実績を教えてください。以下のフォーマットでお願いいたします。\n大会名：順位'])
    
    if club_data['合宿はありますか？'] == 'あります':
        st.markdown("### 🏕️ 合宿情報")
        if pd.notna(club_data['令和6年度の合宿の詳細を教えてください（場所・期間・費用）。']):
            st.info(club_data['令和6年度の合宿の詳細を教えてください（場所・期間・費用）。'])
        else:
            st.info("合宿はありますが、詳細は未定です。")

def categorize_clubs(df):
    """部活動をカテゴリ別にグループ化して並び替え"""
    # 部活動のカテゴリ分類
    categories = {
        'バレーボール': ['中学バレーボール部', '高校バレーボール部'],
        '野球': ['硬式野球部', '軟式野球部', '中学野球部'],
        'バスケットボール': ['女子バスケットボール部', '男子バスケットボール部'],
        'テニス・卓球・バドミントン': ['テニス部', '卓球部', 'バドミントン同好会'],
        '武道・格闘技': ['柔道部', '剣道部'],
        '音楽・芸能': ['吹奏楽部', 'ダンス部', 'チアリーダー部', '合唱同好会'],
        '学術・文化': ['数学同好会', '物理部', '歴史部', '書道部', '写真部', 'ECC'],
        'その他スポーツ': ['水泳部', 'アメリカンフットボール', '陸上部'],
        '趣味・同好会': ['マジック・ジャグリング同好会', '釣り人同好会']
    }
    
    # カテゴリごとに部活動をソート
    sorted_clubs = []
    used_clubs = set()
    
    for category, club_list in categories.items():
        category_clubs = []
        for club_name in club_list:
            if club_name in df['部活動名を教えてください。'].values:
                category_clubs.append(club_name)
                used_clubs.add(club_name)
        
        # カテゴリ内で50音順ソート
        category_clubs.sort()
        sorted_clubs.extend(category_clubs)
    
    # カテゴリに分類されていない部活動を50音順で追加
    remaining_clubs = []
    for club_name in df['部活動名を教えてください。'].values:
        if club_name not in used_clubs:
            remaining_clubs.append(club_name)
    
    remaining_clubs.sort()
    sorted_clubs.extend(remaining_clubs)
    
    # DataFrameを新しい順序で並び替え
    df_sorted = df.set_index('部活動名を教えてください。').loc[sorted_clubs].reset_index()
    return df_sorted

def main():
    st.title("🏫 日本大学第一中学・高等学校　2025年度部活動データ")
    st.markdown("部活動のアイコンをクリックして詳細を確認してください")
    
    # データ読み込み
    try:
        df = load_data()
        # カテゴリ別に並び替え
        df = categorize_clubs(df)
    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {e}")
        return
    
    # セッション状態の初期化
    if 'selected_club' not in st.session_state:
        st.session_state.selected_club = None
    
    # 戻るボタンと詳細表示
    if st.session_state.selected_club is not None:
        if st.button("← 一覧に戻る"):
            st.session_state.selected_club = None
            st.rerun()
        
        # 選択された部活の詳細を表示
        club_data = df[df['部活動名を教えてください。'] == st.session_state.selected_club].iloc[0]
        show_club_detail(club_data)
    else:
        # 部活動一覧の表示
        # フィルタリングオプション
        col1, col2, col3 = st.columns(3)
        with col1:
            gender_filter = st.selectbox("性別制限", ["すべて", "制限なし", "女子のみ", "男子のみ"])
        with col2:
            beginner_filter = st.selectbox("初心者", ["すべて", "歓迎", "要相談"])
        with col3:
            sort_order = st.selectbox("並び順", ["名前順", "部員数順"])
        
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
            # 名前順の場合は、カテゴリ別並び替えを維持
            filtered_df = categorize_clubs(filtered_df)
        
        # グリッド表示
        st.markdown(f"### 該当する部活動: {len(filtered_df)}件")
        
        # 4列のグリッドで表示
        cols_per_row = 4
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
                        if st.button(
                            f"{icon}\n\n{club_name}\n\n👥 {int(club['総部員数'])}人",
                            key=f"club_{idx}",
                            use_container_width=True
                        ):
                            st.session_state.selected_club = club_name
                            st.rerun()

if __name__ == "__main__":
    main()