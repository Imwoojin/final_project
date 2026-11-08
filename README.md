
# 영어 모의고사 자동 채점 및 분석 AI Agent

## 1. 프로젝트 소개

영어 학원에서 학생들의 모의고사 성적을 자동으로 채점하고
성적 분석 및 유사 문제 생성을 지원하는 AI Agent 웹 서비스입니다.

### 주요 기능
- 시험 문제지 PDF, 정답지 PDF, OMR 엑셀 업로드
- PDF에서 정답 및 배점 자동 추출
- 학생별 자동 채점 및 성적 분석
- 평균, 중앙값, 표준편차, 최다 오답 문항 분석
- 채점 결과 엑셀 다운로드
- AI Agent 기반 성적 질의응답
- 최다 오답 문항의 유사 문제 생성
- 대화 세션 내 이전 대화 기억

## 2. 사용 기술

- Python
- Streamlit
- LangChain
- OpenAI GPT-5.4 mini
- pandas
- pdfplumber
- PyMuPDF
- openpyxl

## 3. 기술 선택 이유

### Python 및 pandas
학생별 정답 비교와 통계 계산은 정확성이 중요하므로
LLM이 아닌 Python과 pandas를 활용했습니다.

학생 수를 고정하지 않아 여러 학생의 
데이터도 처리할 수 있도록 구현했습니다.

### pdfplumber 및 PyMuPDF
pdfplumber는 정답 PDF의 표에서 문항 번호, 정답, 배점을
추출하기 위해 사용했습니다.

PyMuPDF는 시험 문제지에서 유사 문제 생성에 필요한
원본 지문을 추출하기 위해 사용했습니다.

### LangChain
사용자의 질문을 이해하고 적절한 성적 분석 Tool을
선택하여 실행하는 Agent를 구축하기 위해 사용했습니다.

### RAG 및 LangGraph를 사용하지 않은 이유
이번 프로젝트는 45개 문항과 정형화된 성적 데이터를
처리하는 것이 핵심입니다.

학생 성적은 pandas로 정확하게 조회하고,
시험 문항은 문항 번호를 기준으로 직접 검색할 수 있으므로
벡터 DB 기반 RAG가 필요하지 않다고 판단했습니다.

또한 복잡한 다중 Agent 작업 흐름보다는
LangChain Tool Calling만으로 요구 기능을 구현할 수 있어
LangGraph를 사용하지 않았습니다.

이러한 구조로 불필요한 복잡성을 줄이고
정확성과 응답 효율성을 확보하고자 했습니다.

### Streamlit
Python 기반으로 웹 인터페이스를 빠르게 구현하고
Streamlit Community Cloud에서 무료로 배포할 수 있어
선택했습니다.

## 4. 실행 방법

1. 필요한 패키지 설치

   pip install -r requirements.txt

2. 프로젝트 루트의 .env 파일에 OPENAI_API_KEY 설정

3. Streamlit 실행

   streamlit run app.py

## 5. 사용 방법

1. 성적 분석 페이지로 이동합니다.
2. 시험 문제지, 정답지, OMR 엑셀을 업로드합니다.
3. 분석 시작 버튼을 클릭합니다.
4. 성적 분석 결과를 확인하고 엑셀 파일을 다운로드합니다.
5. AI 챗봇에 성적 관련 질문을 하거나 유사 문제 생성을 요청합니다.

※ 듣기 문항(1~17번)이 최다 오답인 경우 음성 데이터가
제공되지 않아 유사 문제를 생성할 수 없음을 안내합니다.

## 6. 배포 주소

https://finalproject-bq4tr.streamlit.app/

## 7. 개발자 정보

- 학번: 202235109
- 이름: 임우진
