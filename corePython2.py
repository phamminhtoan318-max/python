# =============================================================================
# PHẦN 1: BẮT LỖI NGOẠI LỆ (TRY - EXCEPT - ELSE - FINALLY)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 1: BẮT LỖI NGOẠI LỆ (TRY - EXCEPT)")
print("=" * 55)

def chia_so(a, b):
    try:
        ket_qua = a / b
    except ZeroDivisionError:
        print("Lỗi: Không thể chia cho 0")
        return None
    except TypeError:
        print("Lỗi: Vui lòng nhập số")
        return None
    else:
        print(f"Phép tính thành công: {a} / {b} = {ket_qua}")
        return ket_qua
    finally:
        print("Kết thúc hàm chia_so")

chia_so(10, 2)
chia_so(10, 0)


# =============================================================================
# PHẦN 2: TOÁN TỬ SỐ HỌC (ARITHMETIC OPERATORS)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 2: TOÁN TỬ SỐ HỌC")
print("=" * 55)

a = 10
b = 5

print(f"{a} + {b} = {a + b}")       # Cộng
print(f"{a} / {b} = {a / b}")       # Chia thực (ra float)
print(f"{a} // {b} = {a // b}")     # Chia lấy phần nguyên
print(f"{a} % {b} = {a % b}")       # Chia lấy phần dư
print(f"2 ** 4 = {2 ** 4}")         # 2 lũy thừa 4 (16)


# =============================================================================
# PHẦN 3: TOÁN TỬ SO SÁNH KÉP & TOÁN TỬ LOGIC
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 3: SO SÁNH KÉP & LOGIC")
print("=" * 55)

tuoi = 22
co_bang_lai = True

# So sánh kép chuẩn Python: 18 <= tuoi <= 60
if 18 <= tuoi <= 60 and co_bang_lai:
    print("Đủ điều kiện lái xe ô tô!")
else:
    print("Chưa đủ điều kiện.")

da_khoa_tai_khoan = False
if not da_khoa_tai_khoan:
    print("Tài khoản đang hoạt động bình thường.")


# =============================================================================
# PHẦN 4: THAO TÁC GHI FILE (WITH OPEN - MODE 'W' VÀ 'A')
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 4: THAO TÁC GHI FILE")
print("=" * 55)

# 1. Mode 'w' (Write): Ghi mới hoàn toàn (ghi đè nếu file đã tồn tại)
with open("danh_sach.txt", "w", encoding="utf-8") as f:
    f.write("Dòng 1: Nguyễn Văn An\n")
    f.write("Dòng 2: Trần Thị Bình\n")

print("Đã tạo và ghi file danh_sach.txt thành công!")

# 2. Mode 'a' (Append): Ghi nối tiếp vào cuối file (giữ nguyên dữ liệu cũ)
with open("danh_sach.txt", "a", encoding="utf-8") as f:
    f.write("Dòng 3: Lê Văn Cường\n")

print("Đã ghi thêm Dòng 3 vào cuối file!")


# =============================================================================
# PHẦN 5: THAO TÁC ĐỌC FILE (3 CÁCH PHỔ BIẾN)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 5: THAO TÁC ĐỌC FILE")
print("=" * 55)

# Cách 1: Đọc toàn bộ nội dung thành 1 chuỗi (.read())
print("--- Cách 1: Đọc toàn bộ (.read()) ---")
with open("danh_sach.txt", "r", encoding="utf-8") as f:
    noi_dung = f.read()
    print(noi_dung)

# Cách 2: Đọc toàn bộ dòng thành 1 List (.readlines())
print("--- Cách 2: Đọc thành danh sách dòng (.readlines()) ---")
with open("danh_sach.txt", "r", encoding="utf-8") as f:
    cac_dong = f.readlines()
    print("List các dòng:", cac_dong)

# Cách 3: Duyệt từng dòng bằng vòng lặp for (Chuẩn nhất & Tiết kiệm RAM)
print("\n--- Cách 3: Duyệt từng dòng bằng for ---")
with open("danh_sach.txt", "r", encoding="utf-8") as f:
    for stt, dong in enumerate(f, start=1):
        print(f"[{stt}] {dong.strip()}")


# =============================================================================
# PHẦN 6: BỘ GIÁ TRỊ BẤT BIẾN (TUPLE) & KỸ THUẬT UNPACKING
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 6: TUPLE & KỸ THUẬT UNPACKING")
print("=" * 55)

# Tuple dùng ngoặc tròn (), giá trị không thể thay đổi sau khi tạo (Immutable)
# DE thường dùng Tuple để lưu cấu hình tĩnh, tọa độ hoặc thông số DB
db_config = ("localhost", 5432, "analytics_dwh")
print(f"Cấu hình Database: {db_config}")

# Kỹ thuật Unpacking (Phân rã tuple thành các biến riêng biệt trong 1 dòng)
host, port, db_name = db_config
print(f"Host: {host} | Port: {port} | DB: {db_name}")

# Hoán đổi giá trị 2 biến siêu nhanh không cần biến tạm
x, y = 10, 20
x, y = y, x
print(f"Sau khi swap: x = {x}, y = {y}")


# =============================================================================
# PHẦN 7: LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP - CLASS & OBJECT)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 7: LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP)")
print("=" * 55)

class DatabaseConnector:
    """Lớp quản lý kết nối và thực thi truy vấn tới cơ sở dữ liệu"""
    
    # Hàm khởi tạo (Constructor), 'self' đại diện cho chính đối tượng được tạo
    def __init__(self, db_type: str, host: str, port: int):
        self.db_type = db_type
        self.host = host
        self.port = port
        self.is_connected = False
        
    def connect(self):
        self.is_connected = True
        print(f"[{self.db_type}] Đã kết nối thành công tới {self.host}:{self.port}")
        
    def execute_query(self, query: str):
        if not self.is_connected:
            raise ConnectionError("Chưa mở kết nối DB!")
        print(f"[{self.db_type}] Đang thực thi truy vấn: {query}")

# Kế thừa (Inheritance): PostgresConnector thừa hưởng toàn bộ logic từ DatabaseConnector
class PostgresConnector(DatabaseConnector):
    def __init__(self, host: str, port: int = 5432):
        super().__init__(db_type="PostgreSQL", host=host, port=port)

# Khởi tạo đối tượng và gọi phương thức
pg_client = PostgresConnector(host="192.168.1.100")
pg_client.connect()
pg_client.execute_query("SELECT COUNT(*) FROM raw_transactions;")


# =============================================================================
# PHẦN 8: GENERATOR & TỪ KHÓA YIELD (XỬ LÝ DỮ LIỆU LỚN, TIẾT KIỆM RAM)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 8: GENERATOR & YIELD (CHỐNG TRÀN RAM)")
print("=" * 55)

# Thay vì nạp toàn bộ 1 triệu bản ghi vào RAM gây tràn bộ nhớ (OOM),
# Generator sản xuất từng dòng một tại thời điểm cần (Lazy Evaluation).
def stream_large_dataset(total_rows: int):
    for i in range(1, total_rows + 1):
        # Từ khóa yield 'tạm dừng' hàm và trả về giá trị, gọi lần sau sẽ chạy tiếp
        yield f"Record_Batch_ID_{i}"

# Tạo generator object
data_stream = stream_large_dataset(5)
print("Kiểu của data_stream:", type(data_stream))

# Duyệt từng phần tử khi cần:
for record in data_stream:
    print(f"  -> Xử lý: {record}")


# =============================================================================
# PHẦN 9: DECORATOR (@) (ĐO LƯỜNG HIỆU SUẤT PIPELINE ETL)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 9: DECORATOR (@) ĐO THỜI GIAN THỰC THI")
print("=" * 55)

import time
import functools

def track_execution_time(func):
    """Decorator tính thời gian chạy của bất kỳ hàm nào"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        print(f"⏱️ [MONITOR] Hàm '{func.__name__}' đã chạy xong trong {duration:.4f} giây")
        return result
    return wrapper

# Áp dụng decorator với ký hiệu @
@track_execution_time
def etl_batch_job(row_count: int):
    # Giả lập công việc ETL tốn thời gian
    print(f"Đang xử lý ETL cho {row_count} dòng dữ liệu...")
    time.sleep(0.5)
    return "SUCCESS"

# Gọi hàm bình thường, decorator sẽ tự động bọc ngoài
job_status = etl_batch_job(100000)
print(f"Kết quả Job: {job_status}")
