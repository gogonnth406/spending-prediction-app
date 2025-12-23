import streamlit as st
import joblib
import numpy as np

# 1. Load Model đã huấn luyện
try:
    model = joblib.load('spending_model.pkl')
except:
    st.error("Không tìm thấy file model. Hãy chạy file train_model.py trước!")
    st.stop()

# 2. Thiết kế giao diện
st.title("💰 AI Gợi Ý Mức Chi Tiêu")
st.write("Nhập thông tin tài chính của bạn để nhận lời khuyên chi tiêu hợp lý.")

# Tạo form nhập liệu
col1, col2 = st.columns(2)
with col1:
    thu_nhap = st.number_input("Thu nhập hàng tháng (VNĐ)", min_value=0, value=10000000, step=1000000)
    nguoi_phu_thuoc = st.number_input("Số người phụ thuộc", min_value=0, value=0, step=1)
with col2:
    tiet_kiem = st.number_input("Tiền tiết kiệm hiện có (VNĐ)", min_value=0, value=50000000, step=1000000)

# 3. Xử lý dự đoán khi bấm nút
if st.button("Dự đoán mức chi tiêu"):
    # Chuẩn bị dữ liệu input
    input_data = np.array([[thu_nhap, tiet_kiem, nguoi_phu_thuoc]])
    
    # Dự đoán
    prediction = model.predict(input_data)[0]
    
    # Hiển thị kết quả
    st.success(f"Mức chi tiêu gợi ý cho bạn là: {int(prediction):,} VNĐ / tháng")
    
    # Logic tư vấn thêm (Rule-based đơn giản)
    ty_le = prediction / thu_nhap
    if ty_le > 0.7:
        st.warning("⚠️ Cảnh báo: Mức chi tiêu này khá cao so với thu nhập!")
    elif ty_le < 0.3:
        st.info("✅ Tuyệt vời: Bạn đang tiết kiệm rất tốt.")
    else:
        st.info("💡 Mức chi tiêu này khá cân đối.")

# Footer
st.markdown("---")
st.caption("Bài tập Machine Learning cơ bản trên nền tảng Cloud")