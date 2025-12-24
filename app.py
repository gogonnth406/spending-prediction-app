import streamlit as st
import pandas as pd
import logic

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Personal Finance AI", page_icon="💰", layout="wide")

# CSS để làm đẹp giao diện (Làm cho giống ảnh mẫu Card trắng)
st.markdown("""
<style>
    .block-container {padding-top: 2rem;}
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("💰 Dự Đoán Tài Chính Cá Nhân")
st.markdown("Nhập mục tiêu của bạn - Trợ lý AI đẹp xinh sẽ giúp bạn tính toán lộ trình chi tiêu hợp lý nhất.")
st.write("---")

# --- LOAD LOGIC ---
model = logic.load_and_train()

# --- INPUT (Cột bên trái) ---
col_input, col_result = st.columns([1, 2])

with col_input:
    st.subheader("📝 Nhập thông tin")
    
    thu_nhap = st.number_input("Thu nhập hàng tháng (VNĐ)", 
                               value=15000000, step=500000, format="%d")
    
    muc_tieu = st.number_input("Mục tiêu tiết kiệm (VNĐ)", 
                               value=50000000, step=1000000, format="%d",
                               help="Ví dụ: Mua xe, mua laptop...")
    
    nguoi_phu_thuoc = st.slider("Số người phụ thuộc", 0, 10, 0)
    
    btn_predict = st.button("🚀 Phân Tích", type="primary", use_container_width=True)

# --- RESULT (Cột bên phải) ---
with col_result:
    if btn_predict:
        # Gọi hàm tính toán
        chi_tieu, tien_du, thang = logic.predict_financial_plan(model, thu_nhap, nguoi_phu_thuoc, muc_tieu)
        
        st.subheader("📊 Kết quả phân tích")
        
        # 1. Hàng hiển thị các con số quan trọng (Metrics)
        m1, m2, m3 = st.columns(3)
        m1.metric("Chi tiêu đề xuất", f"{int(chi_tieu):,} đ", delta="An toàn")
        m2.metric("Tiền dư mỗi tháng", f"{int(tien_du):,} đ", delta="Tích lũy")
        
        if thang > 100:
            m3.metric("Thời gian đạt mục tiêu", "Rất lâu", delta_color="inverse")
        else:
            m3.metric("Thời gian đạt mục tiêu", f"{thang:.1f} tháng", delta="Mục tiêu")

        st.divider()

        # 2. Hai cột: Biểu đồ và Chi tiết
        c_chart, c_detail = st.columns([1.5, 1])
        
        with c_chart:
            st.write("**📈 Lộ trình tiết kiệm dự kiến**")
            # Tạo dữ liệu giả lập lộ trình tích lũy
            months = range(1, int(thang) + 2)
            savings_progress = [min(m * tien_du, muc_tieu) for m in months]
            
            chart_data = pd.DataFrame({
                "Tháng": months,
                "Tài sản tích lũy": savings_progress
            })
            st.area_chart(chart_data, x="Tháng", y="Tài sản tích lũy", color="#4CAF50")
            
        with c_detail:
            st.write("**📋 Phân bổ chi tiêu (Gợi ý)**")
            allocation = logic.get_allocation(chi_tieu)
            for item, amount in allocation.items():
                st.info(f"{item}\n\n**{int(amount):,} đ**")

    else:
        # Màn hình chờ (Hiện ảnh minh họa hoặc text)
        st.info("👈 Vui lòng nhập thông tin bên trái để xem kết quả.")
        st.image("https://cdn.dribbble.com/users/427857/screenshots/16656728/media/64b3c43497d544f80872688757049454.png", caption="Minh họa Dashboard")
