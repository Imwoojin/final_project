
from io import BytesIO
from agent import build_agent

import streamlit as st
import pdfplumber
import pandas as pd

st.title("성적 분석")


# 정답 PDF에서 정답과 배점 추출
def read_answers(pdf_file):
    symbols = {"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5}
    answers = {}

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table[1:]:
                    for i in range(0, len(row), 3):
                        number, answer, score = row[i:i+3]

                        if not number:
                            continue

                        answers[int(number)] = {
                            "answer": symbols[answer.strip()],
                            "score": int(score)
                        }

    return answers


# 1. 사이드바: 데이터 업로드
with st.sidebar:
    st.header("데이터 업로드")

    exam_file = st.file_uploader("시험 문제지", type="pdf")
    answer_file = st.file_uploader("정답지", type="pdf")
    omr_file = st.file_uploader("OMR 결과", type="xlsx")

    start = st.button(
        "분석 시작",
        disabled=not (exam_file and answer_file and omr_file)
    )


# 2. 자동 채점
if start:
    answers = read_answers(answer_file)
    omr = pd.read_excel(omr_file)

    results = omr[["학생명"]].copy()

    for num, info in answers.items():
        col = f"Q{num:02d}"
        results[col] = omr[col] == info["answer"]

    results["총점"] = sum(
        results[f"Q{num:02d}"] * info["score"]
        for num, info in answers.items()
    )

    # 문항별 오답 분석
    question_cols = [f"Q{i:02d}" for i in range(1, 46)]
    wrong_counts = (~results[question_cols]).sum()
    top3 = wrong_counts.sort_values(
        ascending=False, kind="stable"
    ).head(3)

    # 엑셀 요약 데이터
    summary = {
        "평균": round(results["총점"].mean(), 2),
        "중앙값": results["총점"].median(),
        "표준편차": round(results["총점"].std(ddof=0), 2)
    }

    for i, (question, count) in enumerate(top3.items(), 1):
        summary[f"최다 오답 {i}위"] = f"{int(question[1:])}번 ({count}명)"

    summary_df = pd.DataFrame(
        summary.items(), columns=["항목", "값"]
    )

    # 엑셀 파일 생성
    excel = BytesIO()

    with pd.ExcelWriter(excel, engine="openpyxl") as writer:
        summary_df.to_excel(
            writer, sheet_name="채점 결과", index=False
        )
        results.to_excel(
            writer, sheet_name="채점 결과",
            startrow=9, index=False
        )

    # 분석 결과 저장
    st.session_state["excel_data"] = excel.getvalue()
    st.session_state["results"] = results
    st.session_state["answers"] = answers
    st.session_state["exam_pdf"] = exam_file.getvalue()
    st.session_state["chat_history"] = []


# 3. 엑셀 다운로드: 사이드바
if "excel_data" in st.session_state:
    st.sidebar.download_button(
        "엑셀 추출",
        data=st.session_state["excel_data"],
        file_name="채점결과.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# 4. 채점 완료 후 메인 화면 표시
if "results" in st.session_state:
    results = st.session_state["results"]

    st.write("채점 학생 수:", len(results))
    st.dataframe(
        results[["학생명", "총점"]], hide_index=True
    )

    st.subheader("전체 학생 성적 분석")

    st.write("평균:", round(results["총점"].mean(), 2))
    st.write("중앙값:", results["총점"].median())
    st.write(
        "표준편차:", round(results["총점"].std(ddof=0), 2)
    )

    question_cols = [f"Q{i:02d}" for i in range(1, 46)]
    wrong_counts = (~results[question_cols]).sum()
    top3 = wrong_counts.sort_values(
        ascending=False, kind="stable"
    ).head(3)

    st.subheader("가장 많이 틀린 문항 TOP 3")

    for question, count in top3.items():
        st.write(f"{int(question[1:])}번 문항: {count}명 오답")

    # 5. 채팅 Agent
    st.subheader("AI 성적 분석 챗봇")

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("성적에 대해 질문해 주세요"):
        st.session_state["chat_history"].append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                agent = build_agent(results, st.session_state["exam_pdf"])

                response = agent.invoke({
                    "messages": st.session_state["chat_history"]
                })

                answer = response["messages"][-1].content
                st.write(answer)

        st.session_state["chat_history"].append(
            {"role": "assistant", "content": answer}
        )
