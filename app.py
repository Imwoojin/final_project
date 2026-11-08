import streamlit as st

st.set_page_config(page_title="영어 모의고사 평가 Agent")

page = st.navigation([
    st.Page("home.py", title="홈", icon="🏠"),
    st.Page("analysis.py", title="성적 분석", icon="📊")
])

page.run()
