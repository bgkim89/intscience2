import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Function to generate the descriptive text for student records
def generate_student_record_text(element_info, impact_info):
    # This is a placeholder. In a real application, you'd likely
    # use a more sophisticated method, possibly involving an LLM,
    # to generate text that truly reflects the guidelines.
    # For now, it will combine the inputs and apply the rules.

    # Example of how to combine and apply rules for the response based on the prompt:
    text = f"주기율표 원소에 대한 흥미와 탐구 의지를 바탕으로 {element_info}를 심층적으로 조사하고, 해당 원소가 인간 생활 및 기술 발전에 미친 영향을 다각도로 분석하여 {impact_info}에 대해 명확하게 제시함. 이 과정에서 자료를 수집하고 핵심 정보를 선별하는 능력이 향상되었음. 특히, 과학적 지식을 실제 현상과 연결하려는 적극적인 태도가 관찰됨. 글쓰기 활동을 통해 복잡한 과학 개념을 이해하기 쉽게 설명하는 표현력이 크게 발달함. 초기에는 기본적인 정보 나열에 그쳤으나, 과제 수행 후에는 원소의 특성이 사회에 미치는 영향까지 심도 있게 탐구하여 그 의미를 파악하는 뛰어난 역량을 보임. 이러한 탐구 활동은 과학적 사고력을 증진시키고, 정보를 비판적으로 분석하여 새로운 관점을 제시하는 능력을 배양함."
    
    # Apply length constraint (approx 420 chars) - this might require some tuning
    # For this example, I'll just ensure it doesn't exceed a certain length
    # In a real LLM scenario, you'd prompt the LLM to adhere to the length
    if len(text) > 420:
        text = text[:420] + "..." # Truncate and add ellipsis

    # Ensure ending words are from the approved list. This is a simple check;
    # a more robust solution might involve rephrasing or an LLM to guarantee adherence.
    approved_endings = [
        "활동함", "표현함", "설명함", "발표함", "안내함", "제작함", "작성함", "관찰됨", "주장함", "설득함",
        "실천함", "기록함", "작성함", "만듦", "토론함", "구성함", "생활함", "씀", "감상함", "평가함",
        "비교함", "분류함", "나열함", "표시함", "나타냄", "구상함", "구체화함", "선택함", "읽음", "해석함",
        "활용함", "분석함", "이야기함", "보충함", "따라함", "모방함", "정리함", "달성함", "도달함",
        "마무리함", "연결함", "찾음", "발견함", "설습함", "적음", "그림", "파악함", "찾음", "표시함",
        "점검함", "찾아냄", "계획함", "추진함", "보고함", "수행함", "보임", "연습함", "적용함",
        "참참함", "조사함", "발굴함", "제출함", "질문함", "대답함", "체험함", "시청함", "해결함",
        "완성함", "측정함", "자신의 생각을 밝힘", "의견을 나눔", "주장을 펼침", "자료를 수집함",
        "의견을 제시함", "해결법을 제시함", "뛰어남", "도와줌", "자질이 있음"
    ]
    
    # Simple check for the last word; ideally, the generation should ensure this
    last_word = text.strip().split()[-1]
    if last_word not in approved_endings:
        # If the generated text doesn't end with an approved word, append one that makes sense
        # This is a very basic fix; for more complex needs, an LLM would be ideal
        if "향상되었음." in text:
            text = text.replace("향상되었음.", "향상되었음. 뛰어남.")
        elif "관찰됨." in text:
            text = text.replace("관찰됨.", "관찰됨. 보임.")
        elif "발달함." in text:
            text = text.replace("발달함.", "발달함. 보임.")
        elif "배양함." in text:
            text = text.replace("배양함.", "배양함. 보임.")

    return text

st.title("생활기록부 '과목별 세부능력 및 특기사항' 자동 생성기")
st.write("CVS 파일을 업로드하면, B열과 C열의 정보를 바탕으로 D열에 '과목별 세부능력 및 특기사항'이 자동 생성됩니다.")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Ensure B and C columns exist
        if 'B' in df.columns and 'C' in df.columns:
            st.success("파일이 성공적으로 업로드되었습니다. 내용을 처리 중입니다.")

            # Apply the function to create the 'D' column
            df['D'] = df.apply(
                lambda row: generate_student_record_text(row['B'], row['C']), axis=1
            )

            st.subheader("처리된 데이터 미리보기")
            st.dataframe(df)

            csv_output = df.to_csv(index=False, encoding='utf-8-sig') # 'utf-8-sig' for proper Korean encoding in Excel
            st.download_button(
                label="처리된 CSV 파일 다운로드",
                data=csv_output,
                file_name="processed_student_records.csv",
                mime="text/csv",
            )
        else:
            st.error("업로드된 CSV 파일에 'B' 또는 'C' 열이 없습니다. 컬럼명을 확인해주세요.")

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
