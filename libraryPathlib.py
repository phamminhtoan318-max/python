# =============================================================================
# THƯ VIỆN PATHLIB: QUẢN LÝ ĐƯỜNG DẪN & HỆ THỐNG FILE CHUẨN DATA ENGINEER
# =============================================================================
from pathlib import Path

# =============================================================================
# PHẦN 1: KHỞI TẠO PATH & TRÍCH XUẤT THUỘC TÍNH FILE
# =============================================================================
print("\n" + "=" * 60)
print("PHẦN 1: KHỞI TẠO PATH & TRÍCH XUẤT THUỘC TÍNH")
print("=" * 60)

# Dùng Path(__file__).parent để luôn lấy thư mục chứa file code hiện tại
# Dấu '/' được nạp chồng (overload) để nối đường dẫn cực kỳ trực quan
base_dir = Path(__file__).parent
file_path = base_dir / "bank.csv"

print("Đường dẫn tuyệt đối (.resolve):", file_path.resolve())
print("Tên file có phần mở rộng (.name):", file_path.name)        # "bank.csv"
print("Tên file không kèm đuôi (.stem):", file_path.stem)        # "bank"
print("Đuôi mở rộng (.suffix):", file_path.suffix)               # ".csv"
print("Thư mục cha chứa file (.parent):", file_path.parent)

print(f"File có tồn tại không? (.exists()): {file_path.exists()}")
print(f"Đây có phải là file không? (.is_file()): {file_path.is_file()}")
print(f"Đây có phải là thư mục không? (.is_dir()): {file_path.is_dir()}")


# =============================================================================
# PHẦN 2: TỰ ĐỘNG TẠO CÂY THƯ MỤC AN TOÀN (PIPELINE DATA LAKE / STAGING)
# =============================================================================
print("\n" + "=" * 60)
print("PHẦN 2: TỰ ĐỘNG TẠO CÂY THƯ MỤC AN TOÀN (.mkdir)")
print("=" * 60)

# DE thường tổ chức folder: data_lake/raw/bank_transactions/
landing_zone = base_dir / "data_lake" / "raw" / "bank_transactions"

# parents=True: Tự động tạo tất cả thư mục cha nếu chưa có
# exist_ok=True: Không văng lỗi nếu thư mục đã tồn tại từ trước (idempotent)
landing_zone.mkdir(parents=True, exist_ok=True)
print(f"Đã đảm bảo thư mục tồn tại: {landing_zone}")


# =============================================================================
# PHẦN 3: ĐỌC & GHI FILE NHANH 1 DÒNG (.write_text / .read_text)
# =============================================================================
print("\n" + "=" * 60)
print("PHẦN 3: ĐỌC & GHI FILE TỐC HÀNH (.write_text / .read_text)")
print("=" * 60)

readme_file = landing_zone / "pipeline_metadata.txt"

# Ghi file nhanh không cần khối 'with open' cồng kềnh
readme_file.write_text("Source: Core Banking API\nBatch: 2026-11-08\nStatus: Initialized", encoding="utf-8")
print(f"Đã tạo file metadata tại: {readme_file.name}")

# Đọc nội dung file ra chuỗi string
content = readme_file.read_text(encoding="utf-8")
print("Nội dung đọc được:")
print(content)


# =============================================================================
# PHẦN 4: QUÉT TÌM HÀNG LOẠT FILE TỰ ĐỘNG (.glob / .rglob)
# =============================================================================
print("\n" + "=" * 60)
print("PHẦN 4: QUÉT TÌM FILE TỰ ĐỘNG ĐỂ LOAD VÀO PIPELINE (.glob / .rglob)")
print("=" * 60)

# 1. .glob("*.py"): Tìm tất cả file .py ở ngay thư mục hiện tại
print("--- Danh sách các file Python trong thư mục hiện tại (.glob): ---")
for p in base_dir.glob("*.py"):
    print(f"  -> {p.name} (Kích thước: {p.stat().st_size} bytes)")

# 2. .rglob("*.txt"): Tìm đệ quy (recursive) tất cả file .txt ở các thư mục con (bỏ qua .venv)
print("\n--- Quét đệ quy tìm file dữ liệu .txt trong Data Lake: ---")
for txt_file in (base_dir / "data_lake").rglob("*.txt"):
    print(f"  -> Tìm thấy: {txt_file.relative_to(base_dir)}")
