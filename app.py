import streamlit as st
import logic

# --- CẤU HÌNH ---
st.set_page_config(page_title="AI Financial Advisor", page_icon="🤖")

st.title("Ứng Dụng Tư Vấn Tài Chính Cá Nhân")
st.markdown("Hệ thống sử dụng **Machine Learning (Linear Regression)** học từ dữ liệu của **5.000 khách hàng**.")
st.write("---")

# --- TRAIN MODEL ---
with st.spinner('Đang huấn luyện AI với 5.000 bản ghi dữ liệu...'):
    model, score = logic.train_model()

# Hiển thị độ chính xác của Model (Để lòe thầy xíu :D)
st.success(f"✅ Model đã học xong! Độ chính xác (R² Score): **{score*100:.2f}%**")

# --- INPUT ---
col1, col2 = st.columns(2)
with col1:
    thu_nhap = st.number_input("Thu nhập (VNĐ)", value=20000000, step=1000000)
    nguoi_phu_thuoc = st.number_input("Số người phụ thuộc", value=0)
with col2:
    tiet_kiem = st.number_input("Tiền tiết kiệm (VNĐ)", value=50000000, step=1000000)

# --- PREDICT ---
if st.button("🔮 Dự đoán mức chi tiêu an toàn"):
    ket_qua = logic.du_doan_chi_tieu(model, thu_nhap, tiet_kiem, nguoi_phu_thuoc)
    
    # Format tiền tệ
    ket_qua_text = f"{int(ket_qua):,}".replace(",", ".")
    thu_nhap_text = f"{int(thu_nhap):,}".replace(",", ".")
    
    st.markdown(f"### 💡 Gợi ý chi tiêu: <span style='color:green'>{ket_qua_text} VNĐ/tháng</span>", unsafe_allow_html=True)
    
    # Chart visual (Vẽ biểu đồ so sánh)
    chart_data = {
        "Khoản mục": ["Thu Nhập", "Chi Tiêu Gợi Ý", "Dư (Tiết kiệm)"],
        "Số tiền": [thu_nhap, ket_qua, thu_nhap - ket_qua]
    }
    st.bar_chart(data=chart_data, x="Khoản mục", y="Số tiền")
    
    # Lời khuyên
    ty_le = ket_qua / thu_nhap
    if ty_le < 0.5:
        st.info("Bạn quản lý tài chính rất tốt! Dư dả nhiều.")
    elif ty_le > 0.8:
        st.warning("Cảnh báo: Mức chi này hơi cao so với thu nhập!")
    else:
        st.success("Mức chi tiêu cân đối.")

st.write("---")
st.caption("Developed by [Tên Bạn] - Cloud Computing Project")
