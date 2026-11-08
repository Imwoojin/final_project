import streamlit as st
from pathlib import Path

st.set_page_config(page_title="학원 평가 도우미", layout="wide")

# 스타일
st.markdown("""
    <style>
    .main {
        background-color: white;
    }

    .home-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        text-align: center;
    }

    .logo-box {
        margin-top: 30px;
        margin-bottom: 30px;
    }

    .title-text {
        font-size: 32px;
        font-weight: 700;
        color: #1f1f1f;
        margin-top: 20px;
    }

    .subtitle-text {
        font-size: 18px;
        color: #555555;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="home-container">', unsafe_allow_html=True)

logo_path = Path("assets/gachon_logo.png")

if logo_path.exists():
    st.image(str(logo_path), width=180)
else:
    st.markdown("""
        <div class="logo-box">
            <div style="
                width:180px;
                height:180px;
                border:2px solid #999;
                display:flex;
                align-items:center;
                justify-content:center;
                margin:auto;
                font-size:24px;
                color:#666;
            ">
                가천대<br>로고
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="title-text">영어 학원 평가 도우미</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">자동 채점 · 성적 분석 · 유사 문제 생성</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)