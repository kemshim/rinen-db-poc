import streamlit as st
import plotly.graph_objects as go
import numpy as np

# タイトル
st.title('Culture Fit Visualizer (PoC)')

# 企業データの定義
company_data = {
    "株式会社メルカリ風": {"Tech": 95, "Speed": 90, "Team": 40, "Biz": 60},
    "株式会社リクルート風": {"Tech": 60, "Speed": 95, "Team": 50, "Biz": 100},
    "トヨタ自動車株式会社風": {"Tech": 70, "Speed": 40, "Team": 90, "Biz": 80},
    "Google Japan風": {"Tech": 100, "Speed": 70, "Team": 60, "Biz": 80},
}

# サイドバーにスライダーを配置
with st.sidebar:
    st.header('カルチャーパラメータ')
    
    tech_value = st.slider(
        'Tech（技術・品質）',
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )
    
    speed_value = st.slider(
        'Speed（スピード・変化）',
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )
    
    team_value = st.slider(
        'Team（組織・協調）',
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )
    
    biz_value = st.slider(
        'Biz（ビジネス・事業）',
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )
    
    st.divider()
    
    # 比較する企業の選択
    selected_company = st.selectbox(
        '比較する企業を選択',
        options=['なし'] + list(company_data.keys())
    )

# メイン画面
st.header('あなたのカルチャーパラメータ')

# パラメータを表示
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric('Tech（技術・品質）', tech_value)

with col2:
    st.metric('Speed（スピード・変化）', speed_value)

with col3:
    st.metric('Team（組織・協調）', team_value)

with col4:
    st.metric('Biz（ビジネス・事業）', biz_value)

# マッチ度の計算と表示
if selected_company != 'なし':
    st.divider()
    
    # ユーザーのベクトル
    user_vector = np.array([tech_value, speed_value, team_value, biz_value])
    
    # 選択された企業のベクトル
    company_info = company_data[selected_company]
    company_vector = np.array([
        company_info['Tech'],
        company_info['Speed'],
        company_info['Team'],
        company_info['Biz']
    ])
    
    # コサイン類似度を計算
    dot_product = np.dot(user_vector, company_vector)
    norm_user = np.linalg.norm(user_vector)
    norm_company = np.linalg.norm(company_vector)
    
    if norm_user > 0 and norm_company > 0:
        cosine_similarity = dot_product / (norm_user * norm_company)
        match_score = cosine_similarity * 100
    else:
        match_score = 0
    
    # マッチ度を大きく表示
    st.header(f'マッチ度: {match_score:.1f}%')
    st.progress(match_score / 100)

# レーダーチャートを描画
st.header('レーダーチャート')

# レーダーチャート用のデータ準備
categories = ['Tech', 'Speed', 'Team', 'Biz']
values = [tech_value, speed_value, team_value, biz_value]

# Plotlyでレーダーチャートを作成
fig = go.Figure()

# ユーザーの波形（赤、半透明）
fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='あなたのカルチャー',
    line_color='rgb(255, 107, 107)',
    fillcolor='rgba(255, 107, 107, 0.3)'
))

# 選択された企業の波形（青、半透明）
if selected_company != 'なし':
    company_info = company_data[selected_company]
    company_values = [
        company_info['Tech'],
        company_info['Speed'],
        company_info['Team'],
        company_info['Biz']
    ]
    
    fig.add_trace(go.Scatterpolar(
        r=company_values,
        theta=categories,
        fill='toself',
        name=f'{selected_company}のカルチャー',
        line_color='rgb(107, 107, 255)',
        fillcolor='rgba(107, 107, 255, 0.3)'
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )),
    showlegend=True,
    title='カルチャーフィット度'
)

st.plotly_chart(fig, use_container_width=True)
