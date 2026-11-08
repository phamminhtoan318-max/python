import logging
from logging.handlers import RotatingFileHandler

# =============================================================================
# PHẦN 1: CÁC CẤP ĐỘ LOG CƠ BẢN (5 MỨC ĐỘ TỪ NHẸ ĐẾN NẶNG)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 1: CÁC CẤP ĐỘ LOG CƠ BẢN")
print("=" * 55)

# Cấu hình root logger cơ bản: Thời gian | Cấp độ | Thông điệp
logging.basicConfig(
    level=logging.DEBUG,  # Đặt level=DEBUG để nhìn thấy tất cả 5 cấp độ
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.debug("1. DEBUG    : Dùng để soi giá trị biến khi code (vd: x = 10)")
logging.info("2. INFO     : Thông báo tiến trình bình thường (vd: User đăng nhập)")
logging.warning("3. WARNING  : Cảnh báo nguy cơ tiềm ẩn (vd: RAM sắp đầy 85%)")
logging.error("4. ERROR    : Tác vụ thất bại (vd: Không thể gửi email)")
logging.critical("5. CRITICAL : Lỗi cực kỳ nghiêm trọng (vd: Sập kết nối DB)")


# =============================================================================
# PHẦN 2: DÙNG GETLOGGER(__NAME__) ĐỂ GẮN NHÃN TÊN FILE/MODULE
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 2: DÙNG GETLOGGER(__NAME__)")
print("=" * 55)

# Tạo logger riêng cho module này (giúp biết chính xác log phát ra từ file nào)
logger_db = logging.getLogger("DatabaseModule")

def ket_noi_database():
    logger_db.info("Bắt đầu kết nối tới Database...")
    # Giả lập xử lý kết nối
    logger_db.info("Kết nối Database thành công!")

ket_noi_database()


# =============================================================================
# PHẦN 3: XUẤT CẢ CONSOLE (TERMINAL) LẪN FILE NHẬT KÝ
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 3: XUẤT ĐỒNG THỜI RA CONSOLE & FILE APP.LOG")
print("=" * 55)

logger_app = logging.getLogger("AppModule")
logger_app.setLevel(logging.INFO)
logger_app.propagate = False  # Tránh in lặp 2 lần do kế thừa từ root logger

# Định dạng chi tiết: Thời gian | Cấp độ | Tên file:Dòng code - Nội dung
dinh_dang_chi_tiet = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 1. Luồng 1: In ra màn hình Terminal (Console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(dinh_dang_chi_tiet)
logger_app.addHandler(console_handler)

# 2. Luồng 2: Lưu ra file app.log
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setFormatter(dinh_dang_chi_tiet)
logger_app.addHandler(file_handler)

# Thử nghiệm ghi log (vừa hiện lên màn hình, vừa được ghi vào file app.log)
logger_app.info("Hệ thống khởi động thành công!")
logger_app.warning("Bộ nhớ RAM đang ở mức cao!")
print("-> Đã lưu 2 dòng log trên vào file: app.log")


# =============================================================================
# PHẦN 4: ROTATING FILE (XOAY VÒNG CHỐNG TRÀN Ổ CỨNG) & LOGGER.EXCEPTION
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 4: ROTATING FILE & LOGGER.EXCEPTION (CÓ TRACEBACK)")
print("=" * 55)

logger_pay = logging.getLogger("HeThongBanHang")
logger_pay.setLevel(logging.INFO)
logger_pay.propagate = False  # Tránh in lặp 2 lần ra console

dinh_dang_pay = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 1. In ra console cho lập trình viên quan sát
console_pay = logging.StreamHandler()
console_pay.setFormatter(dinh_dang_pay)
logger_pay.addHandler(console_pay)

# 2. Cấu hình RotatingFileHandler:
# - maxBytes=1024*1024 (1MB): Đạt 1MB là tự đổi tên file cũ và tạo file mới
# - backupCount=3: Chỉ lưu tối đa 3 file cũ (server.log.1, server.log.2...), chống đầy ổ cứng
file_xoay_vong = RotatingFileHandler(
    "server.log", maxBytes=1024 * 1024, backupCount=3, encoding="utf-8"
)
file_xoay_vong.setFormatter(dinh_dang_pay)
logger_pay.addHandler(file_xoay_vong)

# Thử nghiệm hàm thanh toán có bắt lỗi:
def thanh_toan(so_tien):
    try:
        logger_pay.info(f"Bắt đầu thanh toán số tiền: {so_tien}$")
        if so_tien <= 0:
            raise ValueError(f"Số tiền không hợp lệ: {so_tien}$")
        
        chiet_khau = 100 / so_tien
        logger_pay.info(f"Thanh toán thành công! Chiết khấu: {chiet_khau:.1f}%")
        
    except Exception:
        # VŨ KHÍ MẠNH NHẤT: logger.exception() tự động in và lưu toàn bộ Call Stack Traceback
        logger_pay.exception("Thanh toán THẤT BẠI do lỗi hệ thống nghiêm trọng!")

thanh_toan(50)  # Giao dịch 1: Thành công
thanh_toan(0)   # Giao dịch 2: Văng lỗi -> In Traceback chi tiết và lưu vào server.log

print("\n-> Đã hoàn tất! Toàn bộ nhật ký lỗi đã được lưu vào: server.log")
