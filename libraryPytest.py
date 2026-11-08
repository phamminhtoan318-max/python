# =============================================================================
# THƯ VIỆN PYTEST: KIỂM THỬ TỰ ĐỘNG PIPELINE DỮ LIỆU CHO DATA ENGINEER
# =============================================================================
# 📌 3 Quy ước bắt buộc của pytest:
# 1. Tên file test: Phải bắt đầu bằng test_*.py hoặc kết thúc bằng *_test.py.
# 2. Tên hàm test: Bắt buộc phải bắt đầu bằng test_*() (ví dụ: def test_clean_price():).
# 3. Cách kiểm tra: Chỉ dùng từ khóa 'assert [Biểu thức kiểm tra]'.
# =============================================================================
import pytest
from datetime import datetime


# =============================================================================
# PHẦN 1: KIỂM THỬ ĐƠN GIẢN VỚI TỪ KHÓA ASSERT
# =============================================================================
# 1. Hàm làm sạch dữ liệu trong pipeline (Hàm cần test)
def clean_currency(raw_price: str) -> float:
    """Biến chuỗi '$1,250.50' thành số thực 1250.5"""
    clean_str = raw_price.replace("$", "").replace(",", "").strip()
    return float(clean_str)


# 2. Viết hàm test kiểm tra tính đúng đắn của logic
def test_clean_currency_chuan():
    assert clean_currency("$100.00") == 100.0
    assert clean_currency("  $1,500.50  ") == 1500.5
    assert clean_currency("0") == 0.0


# =============================================================================
# PHẦN 2: BẮT LỖI NGOẠI LỆ VỚI PYTEST.RAISES (DATA VALIDATION)
# =============================================================================
def validate_age(age: int) -> bool:
    """Kiểm tra độ tuổi hợp lệ trong bảng nhân viên"""
    if age < 0 or age > 120:
        raise ValueError("Độ tuổi không hợp lệ trong thực tế!")
    return True


def test_validate_age_nem_loi_khi_sai():
    # pytest.raises đảm bảo khối code này PHẢI quăng ra đúng lỗi ValueError
    with pytest.raises(ValueError) as exc_info:
        validate_age(-5)
    
    # Kiểm tra thông điệp lỗi có đúng như quy định trong pipeline không
    assert "Độ tuổi không hợp lệ" in str(exc_info.value)


# =============================================================================
# PHẦN 3: TEST HÀNG LOẠT VỚI @PYTEST.MARK.PARAMETRIZE
# =============================================================================
def format_date_for_dwh(date_str: str) -> str:
    """Chuẩn hóa mọi kiểu ngày về định dạng chuẩn YYYY-MM-DD của Data Warehouse"""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError(f"Định dạng ngày không hỗ trợ: {date_str}")


# Chạy test cùng lúc 4 kịch bản khác nhau chỉ trong 1 lần khai báo:
@pytest.mark.parametrize("input_date, expected_date", [
    ("25/12/2026", "2026-12-25"),  # Kiểu Việt Nam DD/MM/YYYY
    ("2026-12-25", "2026-12-25"),  # Kiểu ISO YYYY-MM-DD
    ("12/25/2026", "2026-12-25"),  # Kiểu Mỹ MM/DD/YYYY
    ("01/01/2025", "2025-01-01"),
])
def test_format_date_cac_truong_hop(input_date, expected_date):
    assert format_date_for_dwh(input_date) == expected_date


# =============================================================================
# PHẦN 4: DỮ LIỆU GIẢ LẬP VỚI @PYTEST.FIXTURE (MOCK PIPELINE DATA)
# =============================================================================
# 1. Tạo Fixture: Dữ liệu mẫu giả lập bảng bán hàng nạp vào bộ nhớ test
@pytest.fixture
def sample_sales_data():
    return [
        {"order_id": 1, "product": "Laptop", "amount": 1000, "status": "COMPLETED"},
        {"order_id": 2, "product": "Mouse", "amount": 50, "status": "COMPLETED"},
        {"order_id": 3, "product": "Keyboard", "amount": 80, "status": "CANCELLED"},
    ]


# 2. Hàm nghiệp vụ DE: Tính tổng doanh thu các đơn hoàn thành
def calculate_total_revenue(orders: list) -> float:
    return sum(item["amount"] for item in orders if item["status"] == "COMPLETED")


# 3. Hàm test: Tự động nhận fixture 'sample_sales_data' vào tham số
def test_calculate_total_revenue(sample_sales_data):
    total = calculate_total_revenue(sample_sales_data)
    # Kỳ vọng: 1000 + 50 = 1050 (bỏ qua đơn CANCELLED 80)
    assert total == 1050


# =============================================================================
# CHẠY TEST TRỰC TIẾP (BẤM NÚT RUN TRÊN VS CODE LÀ TỰ CHẠY HẾT TEST)
# =============================================================================
if __name__ == "__main__":
    pytest.main(["-v", __file__])
