import pandas as pd
import great_expectations as gx

# ==============================================================================
# BƯỚC KHỞI TẠO CHUNG: DATA CONTEXT
# ==============================================================================
# gx.get_context(): Khởi tạo Data Context (môi trường làm việc trung tâm của GX).
# -> Nơi quản lý các kết nối nguồn dữ liệu (Data Sources), bộ quy tắc (Suites) và báo cáo.
context = gx.get_context()


# ==============================================================================
# BÀI 1: KIỂM TRA HỒ SƠ NGƯỜI DÙNG (CƠ BẢN: NULL, UNIQUE, RANGE, SET)
# ==============================================================================

# 1. Dữ liệu kiểm thử (có chứa lỗi cố ý để test)
df_users = pd.DataFrame({
    "user_id": [101, 102, 103, 103, 105],      # Lỗi: trùng id 103
    "name": ["Huy", "Lan", "Nam", "Mai", "Hoa"],
    "age": [25, 17, 30, 45, None],             # Lỗi: có tuổi 17 (<18) và None
    "role": ["admin", "member", "hacker", "guest", "member"] # Lỗi: vai trò 'hacker'
})

# 2. Nạp dữ liệu vào GX:
# -> context.data_sources.add_pandas("users_source"): Đăng ký một nguồn dữ liệu kiểu Pandas với tên 'users_source'.
source1 = context.data_sources.add_pandas("users_source")

# -> source1.read_dataframe(df_users): Đọc DataFrame vào và chuyển đổi thành một đối tượng Batch (khối dữ liệu sẵn sàng để test).
batch1 = source1.read_dataframe(df_users)

# 3. Tạo bộ quy tắc (Expectation Suite):
# -> ExpectationSuite: Chiếc hộp/túi chứa gom các quy tắc kiểm thử lại với nhau.
suite1 = gx.ExpectationSuite(name="users_suite")

# [HÀM 1] ExpectColumnValuesToNotBeNull:
# -> Tác dụng: Bắt buộc cột KHÔNG ĐƯỢC CHỨA giá trị rỗng (None / NaN / null).
suite1.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="user_id"))

# [HÀM 2] ExpectColumnValuesToBeUnique:
# -> Tác dụng: Kiểm tra TÍNH DUY NHẤT, không cho phép bất kỳ giá trị nào bị trùng lặp.
# -> Thường dùng cho: ID, Khóa chính (Primary Key), UUID, Mã sinh viên,...
suite1.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="user_id"))

# Kiểm tra tuổi không được null
suite1.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="age"))

# [HÀM 3] ExpectColumnValuesToBeBetween:
# -> Tác dụng: Kiểm tra giá trị số hoặc ngày tháng phải NẰM TRONG KHOẢNG [min_value, max_value].
# -> Ở đây: tuổi phải từ 18 đến 65 (tuổi lao động).
suite1.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="age", min_value=18, max_value=65))

# [HÀM 4] ExpectColumnValuesToBeInSet:
# -> Tác dụng: Kiểm tra giá trị chỉ được phép THUỘC MỘT DANH SÁCH CHO TRƯỚC (Whitelist/Enum).
# -> Nếu xuất hiện giá trị lạ (như 'hacker'), bài test sẽ báo lỗi FAIL ngay.
suite1.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="role",
    value_set=["admin", "member", "guest"]
))

# 4. Chạy kiểm tra dữ liệu:
# -> batch1.validate(suite1): Lấy các quy tắc trong suite1 áp vào dữ liệu batch1 để kiểm tra.
# -> Trả về đối tượng chứa toàn bộ kết quả kiểm thử (PASS/FAIL và chi tiết lỗi).
results1 = batch1.validate(suite1)

print("=" * 60)
print("--- KẾT QUẢ BÀI 1 ---")

# results1.results: Danh sách kết quả của từng Expectation riêng lẻ
for r in results1.results:
    # r.expectation_config.type: Tên loại quy tắc vừa chạy (VD: expect_column_values_to_not_be_null)
    rule = r.expectation_config.type
    
    # r.expectation_config.kwargs.get("column"): Tên cột được kiểm tra (nằm trong kwargs)
    col = r.expectation_config.kwargs.get("column")
    
    # r.success: Thuộc tính Boolean (True nếu đạt chuẩn, False nếu vi phạm)
    status = "✅ PASS" if r.success else "❌ FAIL"
    
    # In ra dòng thông báo: Trạng thái | Tên cột (căn lề trái 8 ký tự) | Tên quy tắc
    print(f"{status} | Cột: {str(col):<8} | Quy tắc: {rule}")
    
    # Nếu bài kiểm tra bị FAIL (r.success == False) thì in thêm chi tiết lỗi
    if not r.success:
        # r.result.get('partial_unexpected_list'): Danh sách các giá trị vi phạm thực tế trong DataFrame
        print(f"   -> Giá trị sai: {r.result.get('partial_unexpected_list')}")


# ==============================================================================
# BÀI 2: ĐƠN HÀNG & CHUỖI (CẤU TRÚC BẢNG, REGEX, ĐỘ DÀI, TỶ LỆ SAI SỐ MOSTLY)
# ==============================================================================

# 1. Dữ liệu đơn hàng mẫu (có lỗi sai format mã đơn và sai độ dài SĐT)
df_orders = pd.DataFrame({
    "order_code": ["ORD-1001", "ORD-1002", "INVALID-99", "ORD-1004", "ORD-1005"], # INVALID-99 sai định dạng regex
    "customer_phone": ["0912345678", "0987654321", "090123", "0333444555", "0888999000"], # 090123 sai độ dài (6 số)
    "amount": [150000, 200000, 50000, 300000, 120000],
    "discount_code": ["SALE10", "SALE20", None, "SALE15", "SALE50"] # 4/5 dòng có mã = 80% (đạt mostly=0.8)
})

# 2. Đăng ký data source mới và nạp dữ liệu đơn hàng
source2 = context.data_sources.add_pandas("orders_source")
batch2 = source2.read_dataframe(df_orders)

# 3. Tạo suite chứa các quy tắc kiểm tra đơn hàng
suite2 = gx.ExpectationSuite(name="orders_suite")

# [HÀM 5] ExpectTableColumnsToMatchOrderedList:
# -> Tác dụng: Kiểm tra CẤU TRÚC BẢNG, đảm bảo bảng có đủ các cột và PHẢI ĐÚNG THỨ TỰ quy định.
suite2.add_expectation(gx.expectations.ExpectTableColumnsToMatchOrderedList(
    column_list=["order_code", "customer_phone", "amount", "discount_code"]
))

# [HÀM 6] ExpectColumnValuesToMatchRegex:
# -> Tác dụng: Kiểm tra chuỗi có KHỚP VỚI BIỂU THỨC CHÍNH QUY (Regex) hay không.
# -> Ở đây: r"^ORD-\d{4}$" yêu cầu chuỗi bắt đầu bằng 'ORD-' và theo sau đúng 4 chữ số.
suite2.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
    column="order_code",
    regex=r"^ORD-\d{4}$"
))

# [HÀM 7] ExpectColumnValueLengthsToBeBetween:
# -> Tác dụng: Kiểm tra ĐỘ DÀI KÝ TỰ (Length) của chuỗi phải nằm trong khoảng [min, max].
# -> Ở đây: số điện thoại phải có từ 10 đến 11 ký tự.
suite2.add_expectation(gx.expectations.ExpectColumnValueLengthsToBeBetween(
    column="customer_phone",
    min_value=10,
    max_value=11
))

# [HÀM 8] Tham số 'mostly' (Tỷ lệ chấp nhận sai số):
# -> Tác dụng: Cho phép một lượng dữ liệu lỗi nhất định mà bài test VẪN PASS.
# -> Ở đây: mostly=0.8 nghĩa là chỉ cần 80% số dòng không bị null là đạt chuẩn (cho phép 20% bị rỗng).
suite2.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
    column="discount_code",
    mostly=0.8
))

# 4. Thực thi kiểm tra bài 2
results2 = batch2.validate(suite2)

print("\n" + "=" * 60)
print("--- KẾT QUẢ BÀI 2 ---")
# results2.success: Kết quả tổng thể (True nếu TẤT CẢ quy tắc đều PASS, False nếu có ít nhất 1 bài FAIL)
print("Toàn bộ bài 2 thành công?", "✅ PASS" if results2.success else "❌ FAIL")

# Lặp qua từng kết quả kiểm tra trong bài 2
for r in results2.results:
    rule = r.expectation_config.type
    # Nếu là kiểm tra toàn bảng thì không có tên cột riêng lẻ -> mặc định hiển thị "TOÀN BẢNG"
    col = r.expectation_config.kwargs.get("column", "TOÀN BẢNG")
    status = "✅ PASS" if r.success else "❌ FAIL"
    print(f"{status} | Cột: {str(col):<15} | Quy tắc: {rule}")
    if not r.success:
        print(f"   -> Giá trị sai: {r.result.get('partial_unexpected_list')}")


# ==============================================================================
# BÀI 3: KIỂM ĐỊNH THỐNG KÊ (KIỂU DỮ LIỆU, GIÁ TRỊ TRUNG BÌNH, MIN/MAX)
# ==============================================================================

# 1. Dữ liệu điểm thi học kỳ của sinh viên
df_scores = pd.DataFrame({
    "student_id": [1, 2, 3, 4, 5, 6],
    "score": [7.5, 8.0, 9.5, 6.0, 8.5, 7.0]
})

# 2. Đăng ký data source mới và nạp dữ liệu điểm số
source3 = context.data_sources.add_pandas("scores_source")
batch3 = source3.read_dataframe(df_scores)

# 3. Tạo suite chứa các quy tắc kiểm tra thống kê
suite3 = gx.ExpectationSuite(name="scores_suite")

# [HÀM 9] ExpectColumnValuesToBeOfType:
# -> Tác dụng: Kiểm tra KIỂU DỮ LIỆU của cột trong DataFrame (ví dụ: float64, int64, str).
# -> Đảm bảo cột điểm số phải là số thực để tính toán được.
suite3.add_expectation(gx.expectations.ExpectColumnValuesToBeOfType(
    column="score",
    type_="float64"
))

# [HÀM 10] ExpectColumnValuesToBeBetween:
# -> Kiểm tra điểm số của từng sinh viên không vượt quá thang điểm [0.0, 10.0]
suite3.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="score",
    min_value=0.0,
    max_value=10.0
))

# [HÀM 11] ExpectColumnMeanToBeBetween:
# -> Tác dụng: Kiểm tra GIÁ TRỊ TRUNG BÌNH CỘNG (Mean / Average) của toàn bộ cột.
# -> Dùng để phát hiện bất thường: nếu điểm trung bình cả lớp < 5.0 hoặc > 8.5 thì có vấn đề.
suite3.add_expectation(gx.expectations.ExpectColumnMeanToBeBetween(
    column="score",
    min_value=5.0,
    max_value=8.5
))

# [HÀM 12] ExpectColumnMinToBeBetween:
# -> Tác dụng: Kiểm tra GIÁ TRỊ NHỎ NHẤT (Min) của cột.
# -> Ở đây: Đảm bảo điểm thấp nhất trong lớp không được là số âm (< 0).
suite3.add_expectation(gx.expectations.ExpectColumnMinToBeBetween(
    column="score",
    min_value=0.0,
    max_value=10.0
))

# 4. Thực thi kiểm tra bài 3
results3 = batch3.validate(suite3)

print("\n" + "=" * 60)
print("--- KẾT QUẢ BÀI 3 ---")
# Tính thử điểm trung bình bằng Pandas để đối chiếu với kỳ vọng của GX
print("Điểm trung bình thực tế:", df_scores["score"].mean())
print("Toàn bộ bài 3 thành công?", "✅ PASS" if results3.success else "❌ FAIL")

# Lặp qua từng kết quả kiểm tra trong bài 3
for r in results3.results:
    rule = r.expectation_config.type
    col = r.expectation_config.kwargs.get("column")
    status = "✅ PASS" if r.success else "❌ FAIL"
    print(f"{status} | Cột: {str(col):<10} | Quy tắc: {rule}")
    if not r.success:
        print(f"   -> Giá trị sai: {r.result.get('partial_unexpected_list')}")
