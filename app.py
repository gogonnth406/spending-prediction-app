import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# --- PHẦN 1: HUẤN LUYỆN MODEL (TRAIN) ---
# Dữ liệu giả lập để dạy AI
# Quy luật ngầm: Chi tiêu = 50% Thu nhập + (Tiết kiệm * 0.05) - (Người phụ thuộc * 1 triệu)
data = {
    'thu_nhap':        [10000000, 15000000, 20000000, 8000000, 50000000, 100000000], # Feature 1
    'tiet_kiem':       [50000000, 20000000, 100000000, 5000000, 200000000, 1000000000], # Feature 2
    'nguoi_phu_thuoc': [0, 1, 2, 0, 3, 4],                                              # Feature 3
    'chi_tieu_goi_y':  [5000000, 7500000, 11000000, 4000000, 25000000, 45000000]        # Label (Cái cần dự đoán)
}

# Tạo DataFrame
df = pd.DataFrame(data)

# Chọn đúng 3 cột làm đầu vào (Input)
X = df[['thu_nhap', 'tiet_kiem', 'nguoi_phu_thuoc']]
y = df['chi_tieu_goi_y']

# Khởi tạo và huấn luyện model Hồi quy tuyến tính
model = LinearRegression()
model.fit(X, y)

# --- PHẦN 2: GIAO DIỆN WEB (STREAMLIT) ---
st.title("💰 Ứng dụng tư vấn Tài chính Cá nhân")
st.write("Nhập thông tin của bạn, Tôi sẽ tính toán mức chi tiêu an toàn hàng tháng.")

# Tạo form nhập liệu (Đúng 3 ô nhập tương ứng với 3 cột lúc train)
col1, col2 = st.columns(2)

with col1:
    thu_nhap = st.number_input("1. Thu nhập hàng tháng (VNĐ)", value=15000000, step=1000000)
    nguoi_phu_thuoc = st.number_input("3. Số người phụ thuộc", value=0, step=1)

with col2:
    tiet_kiem = st.number_input("2. Tiền tiết kiệm hiện có (VNĐ)", value=50000000, step=1000000)

# Nút bấm dự đoán
if st.button("Tính toán mức chi tiêu"):
    # Chuẩn bị dữ liệu đầu vào (Phải đúng thứ tự: Thu nhập -> Tiết kiệm -> Người phụ thuộc)
    input_data = np.array([[thu_nhap, tiet_kiem, nguoi_phu_thuoc]])
    
    try:
        # Gọi model để dự đoán
        ket_qua = model.predict(input_data)[0]
        
        # Làm đẹp kết quả
        ket_qua_dep = f"{int(ket_qua):,}".replace(",", ".")
        
        # Hiện kết quả
        st.success(f"💡 Mức chi tiêu gợi ý: {ket_qua_dep} VNĐ / tháng")
        
        # Logic đưa ra lời khuyên thêm
        if ket_qua / thu_nhap > 0.7:
            st.warning("⚠️ Cảnh báo: Mức chi này chiếm hơn 70% thu nhập!")
        else:
            st.info("✅ Mức chi tiêu này khá an toàn.")
            
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {str(e)}")
