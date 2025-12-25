import streamlit as st
import pandas as pd
import numpy as np
import logic
import random

# --- 1. CẤU HÌNH TRANG & CSS ---
st.set_page_config(page_title="Personal Finance AI", page_icon="💰", layout="wide")

# CSS tùy chỉnh để làm đẹp giao diện (Header xanh, Card trắng, Nền xám)
st.markdown("""
<style>
    /* Đổi màu nền tổng thể sang xám nhạt cho dịu mắt */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Style cho Header xanh */
    .header-style {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 2rem;
        border-radius: 0px 0px 20px 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-style h1 {
        font-family: 'Sans-serif'; 
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 10px;
    }
    .header-style p {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Style cho các Card (Khung trắng) */
    div.css-1r6slb0, div.stVerticalBlock {
        /* CSS này tác động vào container của streamlit */
        gap: 1rem;
    }
    
    /* Làm đẹp metric box */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER (HTML TÙY CHỈNH) ---
st.markdown("""
<div class="header-style">
    <h1>💰 DỰ ĐOÁN TÀI CHÍNH CÁ NHÂN</h1>
    <p>Nhập mục tiêu của bạn - Trợ lý AI đẹp xinh sẽ giúp bạn tính toán lộ trình chi tiêu hợp lý nhất. Giúp bạn nhanh giàu💵</p>
</div>
""", unsafe_allow_html=True)

# --- 3. LOAD LOGIC ---
# (Cache để không phải train lại mô hình mỗi lần reload)
@st.cache_resource
def get_model():
    return logic.load_and_train()

model = get_model()

# --- 4. BỐ CỤC CHÍNH (2 CỘT) ---
col_input, col_result = st.columns([1, 2], gap="medium")

# === CỘT TRÁI: NHẬP LIỆU ===
with col_input:
    with st.container(border=True): # Tạo khung viền
        st.subheader("📝 Nhập thông tin")
        st.write("---")
        
        thu_nhap = st.number_input("Thu nhập hàng tháng (VNĐ)", 
                                   value=15000000, step=500000, format="%d")
        
        muc_tieu = st.number_input("Mục tiêu tiết kiệm (VNĐ)", 
                                   value=50000000, step=1000000, format="%d",
                                   help="Ví dụ: Mua xe, mua laptop...")
        
        # Đã đổi Slider thành Number Input có mũi tên lên xuống theo yêu cầu
        nguoi_phu_thuoc = st.number_input("Số người phụ thuộc", 
                                          min_value=0, max_value=20, value=0, step=1,
                                          help="Con cái, bố mẹ già...")
        
        st.write("") # Khoảng trống
        btn_predict = st.button("🚀 Phân Tích", type="primary", use_container_width=True)

# === CỘT PHẢI: KẾT QUẢ ===
with col_result:
    if btn_predict:
        # Gọi hàm tính toán từ logic.py
        chi_tieu, tien_du, thang = logic.predict_financial_plan(model, thu_nhap, nguoi_phu_thuoc, muc_tieu)
        
        # --- PHẦN 1: CÁC CON SỐ QUAN TRỌNG (METRICS) ---
        st.subheader("📊 Kết quả phân tích")
        m1, m2, m3 = st.columns(3)
        m1.metric("Chi tiêu đề xuất/tháng", f"{int(chi_tieu):,} đ", delta="Mức an toàn")
        m2.metric("Tiền dư để dành/tháng", f"{int(tien_du):,} đ", delta="Tích lũy", delta_color="normal")
        
        if thang > 120: # Hơn 10 năm
            m3.metric("Thời gian đạt mục tiêu", "Rất lâu", delta="Cần điều chỉnh", delta_color="inverse")
        else:
            m3.metric("Thời gian đạt mục tiêu", f"{thang:.1f} tháng", delta="Khả thi")

        st.divider()

        # --- PHẦN 2: BIỂU ĐỒ & CHI TIẾT ---
        c_chart, c_detail = st.columns([1.6, 1])
        
        with c_chart:
            st.write("**📈 Lộ trình tài sản tăng trưởng**")
            # Tạo dữ liệu giả lập lộ trình
            if tien_du > 0:
                months_list = range(1, int(thang) + 5) # Vẽ dư ra vài tháng
                savings_progress = [min(m * tien_du, muc_tieu * 1.1) for m in months_list]
                
                chart_data = pd.DataFrame({
                    "Tháng": months_list,
                    "Tài sản (VNĐ)": savings_progress
                })
                st.area_chart(chart_data, x="Tháng", y="Tài sản (VNĐ)", color="#4CAF50")
            else:
                st.warning("Bạn đang tiêu hết tiền lương! Không thể vẽ biểu đồ tích lũy.")
            
        with c_detail:
            st.write("**📋 Gợi ý phân bổ chi tiêu**")
            allocation = logic.get_allocation(chi_tieu)
            for item, amount in allocation.items():
                st.success(f"{item}\n\n**{int(amount):,} đ**")

        st.divider()

        # --- PHẦN 3: GÓC LỜI KHUYÊN & ĐỘNG LỰC (MỚI) ---
        st.subheader("💡 Góc Lời Khuyên & Động Lực")
        
        # 1. Logic lời khuyên
        ty_le_tiet_kiem = (tien_du / thu_nhap) * 100 if thu_nhap > 0 else 0
        
        if tien_du <= 0:
            advice = "⚠️ **Cảnh báo:** Bạn đang tiêu hết sạch thu nhập! Hãy cắt giảm ngay các khoản 'Vui chơi' và tìm cách tăng thu nhập phụ."
            icon = "🆘"
        elif ty_le_tiet_kiem < 10:
            advice = "⚠️ **Cẩn thận:** Mức tiết kiệm dưới 10% là khá rủi ro. Hãy cố gắng nấu ăn tại nhà thay vì ăn ngoài nhé."
            icon = "🤔"
        elif ty_le_tiet_kiem < 30:
            advice = "✅ **Ổn định:** Bạn đang đi đúng hướng. Để nhanh đạt mục tiêu hơn, hãy thử quy tắc 50/30/20 nghiêm ngặt hơn xem sao."
            icon = "👍"
        else:
            advice = "🔥 **Xuất sắc:** Bạn là bậc thầy quản lý tài chính! Tốc độ tích lũy này rất ấn tượng."
            icon = "🏆"
            
        st.info(f"{icon} {advice}")

        # 2. Random câu trâm ngôn (Quotes)
        quotes = [
            "“Đừng tiết kiệm những gì còn lại sau khi chi tiêu, hãy chi tiêu những gì còn lại sau khi tiết kiệm.” – Warren Buffett",
            "“Một xu tiết kiệm được là một xu kiếm được.” – Benjamin Franklin",
            "“Giàu có không phải là có nhiều tiền, mà là có nhiều lựa chọn.” – Chris Rock",
            "“Đầu tư vào tri thức mang lại lợi nhuận cao nhất.” – Benjamin Franklin",
            "“Tiền bạc là người đầy tớ tốt nhưng là người chủ tồi.”"
        ]
        random_quote = random.choice(quotes)
        st.markdown(f"> *💬 **Câu nói hay:** {random_quote}*")

    else:
        # Màn hình chờ khi chưa bấm nút
        st.info("👈 Bạn hãy nhập thu nhập và mục tiêu ở cột bên trái, rồi bấm nút **'Phân Tích'** nhé!")
        # Placeholder cho đẹp
        st.markdown("""
            <div style="text-align: center; color: #888; padding: 50px;">
                <h3>🤖 AI đang chờ dữ liệu của bạn...</h3>
            </div>
        """, unsafe_allow_html=True)
