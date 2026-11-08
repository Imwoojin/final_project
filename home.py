
import streamlit as st
from pathlib import Path

# 홈 화면 중앙 정렬
left, center, right = st.columns([1, 2, 1])

with center:
    st.write("")

    # 가천대 로고
    logo_path = Path(__file__).parent / "assets" / "gachon_logo.png"

    if logo_path.exists():
        _, logo_col, _ = st.columns([1, 1, 1])
        with logo_col:
            st.image(str(logo_path), width=160)
    else:
        st.markdown(
            "<h3 style='text-align:center;'>가천대 로고</h3>",
            unsafe_allow_html=True
        )

    # 서비스 소개
    st.markdown(
        "<h1 style='text-align:center;'>영어 학원 평가 도우미</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:gray;'>"
        "자동 채점 · 성적 분석 · 유사 문제 생성"
        "</p>",
        unsafe_allow_html=True
    )
