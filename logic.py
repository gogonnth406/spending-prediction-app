import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def load_and_train():
    # Load data
    try:
        # --- SỬA LỖI Ở ĐÂY ---
        # 1. encoding='utf-8-sig': Để xóa ký tự lạ (BOM) ở đầu file nếu dùng Excel
        # 2. skipinitialspace=True: Bỏ qua khoảng trắng thừa sau dấu phẩy
        df = pd.read_csv('dataset.csv', encoding='utf-8-sig', skipinitialspace=True)
        
        # 3. Xóa sạch khoảng trắng ở tên cột (Ví dụ: "ThuNhap " -> "ThuNhap")
        df.columns = df.columns.str.strip()
        
        # 4. Kiểm tra kỹ: Nếu không tìm thấy cột ThuNhap thì tự báo lỗi để nhảy xuống phần except
        if 'ThuNhap' not in df.columns:
            raise ValueError("Không tìm thấy cột ThuNhap")

    except Exception as e:
        # Nếu lỗi file hoặc sai tên cột -> Dùng Data dự phòng
        # (In lỗi ra log để bạn biết nếu cần debug)
        print(f"Lỗi đọc CSV: {e}. Đang dùng dữ liệu mẫu.") 
        
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
        "🏠 Nhà cửa & Ăn uống (50%)": int(tong_chi_tieu * 0.5),
        "☕ Vui chơi & Mua sắm (30%)": int(tong_chi_tieu * 0.3),
        "📚 Phát triển bản thân (20%)": int(tong_chi_tieu * 0.2)
    }

#===========================================================================
# --- PHẦN MỚI: XỬ LÝ DANH SÁCH (BATCH) ---
def predict_batch(model, df_input):
    """
    Hàm này nhận vào DataFrame (file upload), chạy dự đoán cho từng dòng
    và trả về DataFrame mới đã có kết quả.
    """
    # Tạo bản sao để không ảnh hưởng dữ liệu gốc
    df_result = df_input.copy()
    
    # Tạo các list để chứa kết quả
    list_chi_tieu = []
    list_tien_du = []
    list_thang = []
    
    # Duyệt từng dòng
    for index, row in df_result.iterrows():
        # Lấy dữ liệu từng người
        tn = row.get('Thu Nhap', 0)
        mt = row.get('Muc Tieu', 0)
        npt = row.get('Nguoi Phu Thuoc', 0)
        
        # Gọi hàm dự đoán lẻ
        ct, td, th = predict_financial_plan(model, tn, npt, mt)
        
        list_chi_tieu.append(ct)
        list_tien_du.append(td)
        list_thang.append(th)
        
    # Gán kết quả vào cột mới
    df_result['Chi Tiêu Gợi Ý'] = list_chi_tieu
    df_result['Tiền Dư/Tháng'] = list_tien_du
    df_result['Số Tháng Cần'] = list_thang
    
    return df_result
