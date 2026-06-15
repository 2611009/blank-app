import streamlit as st
import pandas as pd

st.title("🏭 웨이퍼 결함 판정 시스템")
st.markdown("웨이퍼의 결함 개수를 입력하세요. `-1`이 입력되면 판정이 자동으로 종료됩니다.")

# 1. 스트림릿 위젯으로 데이터 입력 받기
input_data = st.text_input(
    "결함 개수를 띄어쓰기로 구분하여 입력하세요", 
    value="1 3 2 5 -1 2 0"
)

if input_data:
    try:
        # 입력된 문자열을 정수 리스트로 변환
        raw_defects = [int(x) for x in input_data.split()]
        
        results = []
        stopped_by_minus_one = False
        
        # 핵심 로직 수행
        for idx, defect in enumerate(raw_defects):
            # 규칙 1: -1이 입력되면 즉시 끝냄 (break)
            if defect == -1:
                stopped_by_minus_one = True
                break
                
            # 규칙 2 & 3: 3개 이하는 합격, 3개 초과는 불량
            if defect <= 3:
                status = "합격"
            else:
                status = "불량"
                
            results.append({"No": idx + 1, "결함 수": defect, "판정": status})
        
        # 2. 결과 웹 화면에 깔끔하게 보여주기
        if results:
            df = pd.DataFrame(results)
            st.subheader("📊 최종 판정 결과 테이블")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.subheader("📝 상세 내역")
            for row in results:
                if row["판정"] == "합격":
                    st.success(f"📦 Wafer {row['No']}: 합격 (결함: {row['결함 수']}개)")
                else:
                    st.error(f"❌ Wafer {row['No']}: 불량 (결함: {row['결함 수']}개)")

        # -1로 인해 종료되었음을 알리는 메시지
        if stopped_by_minus_one:
            st.warning(f"⚠️ 규칙에 따라 -1 입력 이후의 데이터는 판정하지 않고 종료되었습니다.")
                    
    except ValueError:
        st.error("🚨 올바른 숫자 형식으로 입력해주세요. (숫자와 공백만 입력 가능)")