import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def train_model():
    """
    Tạo ra dataset giả lập 5000 người dùng để train model xịn hơn.
    """
    np.random.seed(42) # Giữ cố định random để kết quả nhất quán
    n_samples = 5000
    
    # 1. Sinh dữ liệu ngẫu nhiên
    # Thu nhập từ 5 triệu đến 100 triệu
    thu_nhap = np.random.randint(5000000, 100000000, n_samples)
    
    # Số người phụ thuộc từ 0 đến 5 người
    nguoi_phu_thuoc = np.random.randint(0, 6, n_samples)
    
    # Tiết kiệm: Thường người thu nhập cao sẽ có tiết kiệm cao (nhưng có biến động)
    tiet_kiem = (thu_nhap * np.random.uniform(0.1, 5.0, n_samples)).astype(int)
    
    # 2. Tạo quy luật chi tiêu (Công thức ngầm + Nhiễu ngẫu nhiên noise)
    # Quy luật: Chi tiêu ~ 55% thu nhập + 1.5 triệu/người phụ thuộc - Nhích nhẹ nếu tiết kiệm quá ít
    # Thêm noise (nhiễu) để dữ liệu giống thật (không ai giống ai 100%)
    noise = np.random.normal(0, 1000000, n_samples) # Biến động +/- 1 triệu
    
    chi_tieu = (thu_nhap * 0.55) + (nguoi_phu_thuoc * 1500000) + noise
    
    # Đảm bảo chi tiêu không âm và không vượt quá thu nhập (trừ trường hợp vay nợ - ở đây ta bỏ qua)
    chi_tieu = np.maximum(chi_tieu, 3000000) # Tối thiểu sống là 3 triệu
    chi_tieu = np.minimum(chi_tieu, thu_nhap * 0.95) # Không tiêu hết sạch 100%
    
    # 3. Đóng gói vào DataFrame
    df = pd.DataFrame({
        'thu_nhap': thu_nhap,
        'tiet_kiem': tiet_kiem,
        'nguoi_phu_thuoc': nguoi_phu_thuoc,
        'chi_tieu_goi_y': chi_tieu
    })
    
    # 4. Train Model
    X = df[['thu_nhap', 'tiet_kiem', 'nguoi_phu_thuoc']]
    y = df['chi_tieu_goi_y']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Tính độ chính xác (R-squared) để khoe lên web
    score = model.score(X, y)
    
    return model, score

def du_doan_chi_tieu(model, thu_nhap, tiet_kiem, nguoi_phu_thuoc):
    input_data = np.array([[thu_nhap, tiet_kiem, nguoi_phu_thuoc]])
    ket_qua = model.predict(input_data)[0]
    return max(0, ket_qua) # Đảm bảo không âm