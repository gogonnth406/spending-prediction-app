import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def load_and_train():
    # Load data
    try:
        df = pd.read_csv('dataset.csv')
    except:
        # Data dự phòng nếu lỗi file
        df = pd.DataFrame({
            'ThuNhap': [5000000, 10000000, 20000000],
            'NguoiPhuThuoc': [0, 1, 2],
            'ChiTieuLyTuong': [4500000, 7000000, 12000000]
        })

    X = df[['ThuNhap', 'NguoiPhuThuoc']]
    y = df['ChiTieuLyTuong']
    
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_financial_plan(model, thu_nhap, nguoi_phu_thuoc, muc_tieu_tiet_kiem):
    # 1. AI dự đoán mức chi tiêu an toàn
    input_data = np.array([[thu_nhap, nguoi_phu_thuoc]])
    chi_tieu_goi_y = model.predict(input_data)[0]
    
    # Logic thực tế:
    # Nếu lương < 5tr thì chi tiêu = lương (không dư)
    if thu_nhap <= 5000000:
        chi_tieu_goi_y = thu_nhap
    else:
        # Chặn trên: Chi tiêu tối đa 90% thu nhập
        chi_tieu_goi_y = min(chi_tieu_goi_y, thu_nhap * 0.9)
        # Chặn dưới: Không được thấp hơn 3tr (mức sống tối thiểu)
        chi_tieu_goi_y = max(chi_tieu_goi_y, 3000000)

    # 2. Tính toán tiền dư
    tien_du_hang_thang = thu_nhap - chi_tieu_goi_y
    
    # 3. Tính thời gian đạt mục tiêu (tháng)
    if tien_du_hang_thang <= 0:
        so_thang_can = 999 # Không bao giờ đạt được
    else:
        so_thang_can = muc_tieu_tiet_kiem / tien_du_hang_thang
        
    return chi_tieu_goi_y, tien_du_hang_thang, so_thang_can

def get_allocation(tong_chi_tieu):
    # Chia tiền chi tiết
    return {
        "🏠 Nhà cửa & Ăn uống (50%)": tong_chi_tieu * 0.5,
        "☕ Vui chơi & Mua sắm (30%)": tong_chi_tieu * 0.3,
        "📚 Phát triển bản thân (20%)": tong_chi_tieu * 0.2
    }
