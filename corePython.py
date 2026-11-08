# =============================================================================
# PHẦN 1: BIẾN, KIỂU DỮ LIỆU & CẮT CHUỖI (SLICING)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 1: BIẾN, KIỂU DỮ LIỆU & CẮT CHUỖI")
print("=" * 55)

name = " Python "
age = 20
gpa = 2.8
is_activate = True

clean_name = name.strip().title()
print(f"Xin chào {clean_name}, năm nay bạn {age} tuổi!")

s = "Python3"
print(f"Ký tự đầu tiên của s là: {s[0]}")
print(f"Ký tự cuối cùng của s là: {s[-1]}")
print("Lấy từ index 0 đến 5:", s[0:6])
print("Đảo ngược toàn bộ chuỗi:", s[::-1])


# =============================================================================
# PHẦN 2: CÂU ĐIỀU KIỆN (IF - ELIF - ELSE) & TERNARY OPERATOR
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 2: CÂU ĐIỀU KIỆN (IF - ELIF - ELSE)")
print("=" * 55)

score = 8

if score >= 9:
    grade = "Xuất sắc"
elif score >= 8:
    grade = "Giỏi"
elif score >= 7:
    grade = "Khá"
elif score >= 5:
    grade = "Trung bình"
else:
    grade = "Yếu"

print(f"Điểm {score} tương ứng với xếp loại: {grade}")

# Toán tử 3 ngôi (Ternary Operator)
status = "Đỗ" if score >= 5 else "Không đỗ"
print(f"Kết quả môn học: {status}")


# =============================================================================
# PHẦN 3: VÒNG LẶP (RANGE, ENUMERATE, ZIP)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 3: VÒNG LẶP (RANGE, ENUMERATE, ZIP)")
print("=" * 55)

print("Các số lẻ từ 1 đến 9:")
for i in range(1, 10, 2):
    print(i, end=" ")
print("\n")

tasks = ["Học Python", "Làm bài tập", "Đi ngủ"]
for index, task in enumerate(tasks, start=1):
    print(f"Công việc {index}: {task}")

print()
names = ["Sam", "John", "Peter"]
points = [10, 20, 30]
for name, point in zip(names, points):
    print(f"{name} có {point} điểm")


# =============================================================================
# PHẦN 4: DANH SÁCH (LIST) & LIST COMPREHENSION
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 4: DANH SÁCH (LIST) & LIST COMPREHENSION")
print("=" * 55)

number = [1, 2, 3]
number.append(4)
print(f"List sau khi append: {number}")

number.insert(1, 1.5)
print(f"List sau khi insert: {number}")

number.remove(1.5)
print(f"List sau khi remove: {number}")

last_number = number.pop()
print(f"List sau khi pop: {number}, phần tử bị xóa là: {last_number}")

# List Comprehension
squares = [x ** 2 for x in range(1, 6)]
print(f"List bình phương (1-5): {squares}")


# =============================================================================
# PHẦN 5: TẬP HỢP (SET) & TỪ ĐIỂN (DICTIONARY)
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 5: TẬP HỢP (SET) & TỪ ĐIỂN (DICTIONARY)")
print("=" * 55)

raw_data = [1, 2, 2, 3, 4, 4, 4, 5]
clean_data = list(set(raw_data))
print("Dữ liệu sau khi lọc trùng:", clean_data)

student = {
    "name": "Toan",
    "major": "IT",
    "gpa": 3.8
}

email = student.get("email", "Chưa cập nhật")
print(f"Email của {student['name']}: {email}")

print("Duyệt thông tin student:")
for key, value in student.items():
    print(f"  {key}: {value}")


# =============================================================================
# PHẦN 6: HÀM (FUNCTIONS), *ARGS, **KWARGS & LAMBDA
# =============================================================================
print("\n" + "=" * 55)
print("PHẦN 6: HÀM, *ARGS, **KWARGS & LAMBDA")
print("=" * 55)

# 1. *args: Gom mọi tham số vị trí vào 1 Tuple
def tinh_tong(*numbers):
    return sum(numbers)

print(f"Tổng của 1, 2, 3 là: {tinh_tong(1, 2, 3)}")

# 2. **kwargs: Gom mọi tham số key=value vào 1 Dict
def show_info(**details):
    for key, value in details.items():
        print(f"  {key}: {value}")

print("Thông tin chi tiết:")
show_info(name="Toan", age=20, major="IT")

# 3. Lambda: Hàm ẩn danh dùng để sắp xếp danh sách phức tạp
danh_sach = [("Nam", 7), ("Hoa", 9), ("Bình", 8)]
danh_sach_sap_xep = sorted(danh_sach, key=lambda x: x[1], reverse=True)
print("Top điểm cao xếp theo điểm giảm dần:", danh_sach_sap_xep)
