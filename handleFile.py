# =============================================================================
# THAO TÁC FILE NÂNG CAO CHO DATA ENGINEER: JSON & CSV
# =============================================================================
import json
import csv
from pathlib import Path

base_dir = Path(__file__).parent


# =============================================================================
# PHẦN 1: XỬ LÝ ĐỊNH DẠNG JSON (API PAYLOAD & SEMI-STRUCTURED DATA)
# =============================================================================
# 📌 Quy tắc ghi nhớ:
# - Có chữ 's' (String) -> Làm việc với biến/chuỗi text trong RAM: dumps(), loads()
# - Không có chữ 's'    -> Làm việc trực tiếp với File trên ổ đĩa: dump(), load()
# =============================================================================
print("\n" + "=" * 60)
print("PHẦN 1: XỬ LÝ FILE & CHUỖI JSON (API PAYLOAD)")
print("=" * 60)

user_data = {
    "id": 101,
    "name": "Toàn Phạm",
    "is_admin": True,
    "skills": ["Python", "SQL", "Docker"],
    "bio": None  # Trong JSON sẽ tự động biến thành null
}

# 1. Chuyển Python Dict -> Chuỗi JSON (json.dumps)
# Mẹo DE: ensure_ascii=False để giữ tiếng Việt chuẩn; indent=4 để format đẹp
json_str = json.dumps(user_data, ensure_ascii=False, indent=4)
print("Chuỗi JSON sau khi serialize:\n", json_str)

# 2. Chuyển Chuỗi JSON -> Python Dict (json.loads)
parsed_dict = json.loads(json_str)
print("\nKiểu dữ liệu sau khi parse:", type(parsed_dict))  # <class 'dict'>

# 3. Ghi dữ liệu trực tiếp vào file JSON trên ổ cứng (json.dump)
json_file_path = base_dir / "user.json"
with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(user_data, f, ensure_ascii=False, indent=4)
print(f"\nĐã ghi file JSON thành công: {json_file_path.name}")

# 4. Đọc trực tiếp từ file JSON ra Python Dict (json.load)
with open(json_file_path, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(f"Đọc từ file ra: Tên = {loaded_data['name']}, Kỹ năng = {loaded_data['skills']}")


# =============================================================================
# PHẦN 2: XỬ LÝ FILE CSV DẠNG DANH SÁCH (CSV.WRITER & CSV.READER)
# =============================================================================
print("\n" + "=" * 60)
print("PHẦN 2: XỬ LÝ CSV DẠNG DANH SÁCH (CSV.WRITER & CSV.READER)")
print("=" * 60)

raw_matrix = [
    ["ID", "Tên", "Điểm"],
    [1, "Nguyễn Văn An", 8.5],
    [2, "Trần Thị Bình", 9.0],
    [3, "Lê Văn Cường", 7.0]
]

csv_list_path = base_dir / "students.csv"

# Ghi file CSV dạng danh sách dòng (newline="" để tránh dòng trống trên Windows/Linux)
with open(csv_list_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(raw_matrix)
print(f"Đã ghi file: {csv_list_path.name}")

# Đọc file CSV dạng danh sách
print("Nội dung đọc từng dòng:")
with open(csv_list_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  -> {row}")


# =============================================================================
# PHẦN 3: XỬ LÝ CSV DẠNG TỪ ĐIỂN (DICTWRITER & DICTREADER - KHUYÊN DÙNG)
# =============================================================================
print("\n" + "=" * 60)
print("PHẦN 3: XỬ LÝ CSV DẠNG DICT (DICTWRITER & DICTREADER)")
print("=" * 60)

students_dict = [
    {"id": 1, "name": "Toàn", "score": 9.5},
    {"id": 2, "name": "Hoa", "score": 8.0},
    {"id": 3, "name": "Nam", "score": 7.5}
]

csv_dict_path = base_dir / "students_dict.csv"
fields = ["id", "name", "score"]

# 1. Ghi CSV dạng Dict
with open(csv_dict_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()      # Tự động ghi dòng tiêu đề cột
    writer.writerows(students_dict)
print(f"Đã ghi file DictWriter: {csv_dict_path.name}")

# 2. Đọc CSV dạng Dict (Truy xuất qua tên cột trực quan, không lo bị nhầm index)
print("Đọc theo tên cột với DictReader:")
with open(csv_dict_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  -> Học sinh: {row['name']:<10} | Điểm: {row['score']}")
