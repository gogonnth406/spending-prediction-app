import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Huấn luyện Model (Chạy ngầm)
data = {
    'thu_nhap':        [10000000, 15000000, 20000000, 8000000, 50000000, 100000000],
    'tiet_kiem':       [50000000, 20000000, 100000000, 5000000, 200000000, 1000000000],
    'nguoi_phu_thuoc': [0, 1, 2, 0, 3, 4],
    'chi_tieu_goi_y':  [5000000, 7500000, 11000000, 4000000, 25000000, 45000000] 
}
df = pd.DataFrame(data)
model = LinearRegression()
model.fit(df[['thu_nhap', 'tiet_kiem', 'nguoi_phu_thuoc']], df['chi_tieu_goi_y'])

# 2. Giao diện Web
st.title("💸 Ứng dụng Gợi ý Chi tiêu (Running on Azure)")
st.write("Nhập thông tin để AI tính toán mức chi tiêu hợp lý.")

col1, col2 = st.columns(2)
with col1:
    thu_nhap = st.number_input("Thu nhập (VNĐ)", value=10000000, step=1000000)
    nguoi = st.number_input("Số người phụ thuộc", value=0)
with col2:
    tiet_kiem = st.number_input("Tiền tiết kiệm (VNĐ)", value=50000000)

if st.button("Tính toán"):
    du_doan = model.predict([[thu_nhap, tiet_kiem, nguoi]])[0]
    st.success(f"Mức chi tiêu gợi ý: {int(du_doan):,} VNĐ")