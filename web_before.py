import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Set the following option to avoid matplotlib warnings
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

# Set page layout
st.set_page_config(
    page_title="불량 여부 예측",
    layout="wide"  # 넓은 레이아웃 설정
)

# CSV 파일 로드
def load_data():
    data = pd.read_csv("/home/piai/빅데이터/빅데이터 프로젝트/B3_반도체/control_para(이결제거).csv")  # 파일 경로를 수정하세요
    return data

# 불량 예측
def predict_defect():
    # 모델 연결 전 임시 확률 생성
    defect_prob = np.random.uniform(0, 1)  # 0부터 1 사이의 랜덤 확률 생성
    return "불량" if defect_prob <= 0.03 else "양품"  # 3% 확률로 불량 여부 예측

# Streamlit 앱 개발
def main():
    st.title("불량 여부 예측")

    # CSV 파일 로드
    data = load_data()

    input_all_list = pd.DataFrame()
    input_defective_list = pd.DataFrame()
    input_perfect_list = pd.DataFrame()

    avg_columns = ['Temp_OXid', 'ppm', 'Pressure', 'Oxid_time', 'Temp_implantation', 'temp_HMDS_bake']

    if st.button("시작"):
        for index in range(len(data)):
            placeholder = st.empty()
            data_row = data.iloc[index]
            # 불러온 전체 웨이퍼 정보 저장
            input_all_list = input_all_list.append(data_row, ignore_index=True)
            # 불러온 불량 웨이퍼 정보 저장
            # input_defective_list = input_defective_list.append(data_row, ignore_index=True)
            # 불러온 양품 웨이퍼 정보 저장
            # input_perfect_list = input_perfect_list.append(data_row, ignore_index=True)

            no_die_value = data_row["No_Die"]
            prediction = predict_defect()
            if prediction == "불량":
                input_defective_list = input_defective_list.append(data_row, ignore_index=True)
            elif prediction == "양품":
                input_perfect_list = input_perfect_list.append(data_row, ignore_index=True)

            with placeholder.container():
                st.write(no_die_value, "  ", prediction)
                col1, col2, col3, col4, col5 = st.columns(5)  # 두 열로 나누기
                
                with col1.container():
                    st.write("평균:")
                    avg_values = input_all_list[avg_columns].mean().round(2)
                    st.write(avg_values)

                with col2.container():
                    st.write("불량률:")
                    total_count = len(data)
                    defective_count = len(input_defective_list)
                    perfect_count = len(input_perfect_list)
                    pie_chart_data = [defective_count / total_count, perfect_count / total_count]
                    labels = ['불량품', '양품']
                    plt.pie(pie_chart_data, labels=labels, autopct='%1.1f%%', startangle=140)
                    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    st.pyplot()

                with col3.container():
                    if len(input_defective_list) != 0:
                        st.write("불량 평균:")
                        avg_values = input_defective_list[avg_columns].mean().round(2)
                        st.write(avg_values)

                with col4.container():
                    if len(input_defective_list) != 0:
                        st.write("불량 웨이퍼 정보")
                    # avg_values = input_defective_list[avg_columns].mean().round(2)
                        st.write(input_defective_list)

            time.sleep(0.5)
            placeholder.empty()

if __name__ == "__main__":
    main()
