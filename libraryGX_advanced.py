"""
================================================================================
HỆ THỐNG NÂNG CAO TRONG GREAT EXPECTATIONS (GX 1.x) - PRODUCTION & PIPELINE
================================================================================
Bao gồm 3 phần chính mà môi trường doanh nghiệp thực tế sử dụng:
1. Báo cáo HTML trực quan (Data Docs) & Checkpoint tự động hóa
2. Kiểm tra trực tiếp trên Database SQL (SQLite / PostgreSQL)
3. Thiết lập Data Quality Gate (Chặn luồng ETL / Gửi cảnh báo khi lỗi)
"""

import sqlite3
import pandas as pd
import great_expectations as gx
from great_expectations.checkpoint import UpdateDataDocsAction

# ==============================================================================
# PHẦN 1: CHECKPOINT & DATA DOCS (TỰ ĐỘNG SINH BÁO CÁO HTML TRỰC QUAN)
# ==============================================================================
print("=" * 70)
print("PHẦN 1: CHẠY CHECKPOINT VÀ TỰ ĐỘNG XUẤT BÁO CÁO HTML (DATA DOCS)")
print("=" * 70)

# 1. Khởi tạo Context
context = gx.get_context()

# 2. Chuẩn bị dữ liệu mẫu (Khách hàng)
df_customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "email": ["user1@gmail.com", "user2@gmail.com", "invalid_email_format", "user4@gmail.com"],
    "balance": [500.0, 1200.0, -50.0, 300.0]  # Lỗi: balance < 0 và email sai định dạng
})

# 3. Tạo Data Source & Batch Definition (Cách GX 1.x kết nối dữ liệu cho Checkpoint)
source_pandas = context.data_sources.add_pandas("customer_source")
asset_pandas = source_pandas.add_dataframe_asset("customer_asset")
batch_def_pandas = asset_pandas.add_batch_definition_whole_dataframe("customer_batch_def")

# 4. Tạo bộ quy tắc (Expectation Suite)
suite_customer = context.suites.add(gx.ExpectationSuite(name="customer_suite"))
suite_customer.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id"))
suite_customer.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
    column="email",
    regex=r"^[\w\.-]+@[\w\.-]+\.\w+$"
))
suite_customer.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="balance",
    min_value=0.0,
    max_value=1000000.0
))

# 5. Tạo Validation Definition (Cầu nối giữa Dữ liệu & Quy tắc)
val_def_customer = context.validation_definitions.add(
    gx.ValidationDefinition(
        name="customer_val_def",
        data=batch_def_pandas,
        suite=suite_customer
    )
)

# 6. Tạo Checkpoint (Quy trình tự động: Kiểm tra + Tự động cập nhật Data Docs)
checkpoint_customer = context.checkpoints.add(
    gx.Checkpoint(
        name="customer_checkpoint",
        validation_definitions=[val_def_customer],
        actions=[
            # Action: Tự động render báo cáo HTML sau mỗi lần chạy
            UpdateDataDocsAction(name="update_docs_action")
        ]
    )
)

# 7. Thực thi Checkpoint với dữ liệu thực tế
print("-> Đang chạy kiểm thử qua Checkpoint...")
cp_result = checkpoint_customer.run(batch_parameters={"dataframe": df_customers})

print(f"-> Kết quả Checkpoint đạt chuẩn: {cp_result.success}")

# 8. Sinh và lấy đường dẫn trang web báo cáo Data Docs
docs_info = context.build_data_docs()
print("\n🎉 [DATA DOCS] Đã sinh thành công trang báo cáo HTML trực quan:")
for site_name, site_url in docs_info.items():
    print(f"   Trang web: {site_url}")
print("-> Bạn có thể copy đường dẫn 'file://...' dán vào trình duyệt để xem dashboard giao diện cực đẹp!")


# ==============================================================================
# PHẦN 2: KIỂM TRA TRỰC TIẾP TRÊN CƠ SỞ DỮ LIỆU SQL (KHÔNG DÙNG PANDAS)
# ==============================================================================
print("\n" + "=" * 70)
print("PHẦN 2: KIỂM TRA TRỰC TIẾP TRÊN CƠ SỞ DỮ LIỆU SQL (SQLITE)")
print("=" * 70)

# 1. Tạo một cơ sở dữ liệu SQLite thực tế bằng code Python
db_file = "ecommerce.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, price REAL, stock INTEGER)")
cursor.execute("DELETE FROM products")
cursor.executemany(
    "INSERT INTO products VALUES (?, ?, ?, ?)",
    [
        (1, "Bàn phím cơ", 1500000, 20),
        (2, "Chuột Gaming", 800000, 15),
        (3, "Màn hình 4K", -50000, 5),   # Lỗi: Giá âm (-50000)
        (4, "Tai nghe", 1200000, -2)       # Lỗi: Tồn kho âm (-2)
    ]
)
conn.commit()
conn.close()

# 2. Kết nối GX với SQLite thông qua SQLAlchemy connection string
# (Trong thực tế bạn có thể thay bằng 'postgresql://user:pass@host:5432/db')
sql_source = context.data_sources.add_sqlite("sqlite_source", connection_string=f"sqlite:///{db_file}")

# 3. Trỏ tới bảng 'products' trong Database
product_asset = sql_source.add_table_asset(name="product_table_asset", table_name="products")
batch_def_sql = product_asset.add_batch_definition_whole_table("product_sql_batch")

# 4. Định nghĩa quy tắc cho bảng SQL
suite_sql = context.suites.add(gx.ExpectationSuite(name="product_sql_suite"))
suite_sql.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="price",
    min_value=0.0,
    max_value=100000000.0
))
suite_sql.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="stock",
    min_value=0,
    max_value=100000
))

# 5. Tạo Validation Definition & Checkpoint cho SQL
val_def_sql = context.validation_definitions.add(
    gx.ValidationDefinition(
        name="sql_val_def",
        data=batch_def_sql,
        suite=suite_sql
    )
)
checkpoint_sql = context.checkpoints.add(
    gx.Checkpoint(name="sql_checkpoint", validation_definitions=[val_def_sql])
)

# 6. Chạy kiểm tra: GX sẽ thực thi query SQL trực tiếp trên database!
print("-> Đang chạy kiểm thử SQL trên Database...")
sql_result = checkpoint_sql.run()
print(f"-> Kiểm thử SQL thành công: {sql_result.success}")

for run_key, val_res in sql_result.run_results.items():
    for item in val_res.results:
        col = item.expectation_config.kwargs.get("column")
        stt = "✅ PASS" if item.success else "❌ FAIL"
        unexpected = item.result.get("partial_unexpected_list")
        print(f"   {stt} | Cột: {col:<8} | Giá trị vi phạm trên DB: {unexpected}")


# ==============================================================================
# PHẦN 3: DATA QUALITY GATE (NGĂN CHẶN PIPELINE ETL KHI DỮ LIỆU LỖI)
# ==============================================================================
print("\n" + "=" * 70)
print("PHẦN 3: ỨNG DỤNG DATA QUALITY GATE TRONG LUỒNG ETL TỰ ĐỘNG")
print("=" * 70)

def etl_pipeline_simulation(run_validation_checkpoint):
    """
    Mô phỏng một hàm chạy trong Airflow / Celery / Cronjob:
    - Nếu GX báo dữ liệu lỗi -> Ngắt luồng và báo động đỏ.
    - Nếu GX báo PASS -> Cho phép nạp dữ liệu vào Data Warehouse.
    """
    print("-> Bước 1: Trích xuất dữ liệu thô (Extract)...")
    
    print("-> Bước 2: Kiểm định chất lượng bằng Great Expectations (Validate)...")
    check_result = run_validation_checkpoint.run()
    
    if not check_result.success:
        print("🚨 [ALERT] DỮ LIỆU BỊ LỖI! Dừng luồng ETL ngay lập tức để bảo vệ hệ thống!")
        print("📨 [SEND NOTIFICATION] Gửi cảnh báo tới kênh Slack #data-alerts / Email Kỹ sư...")
        return False
    
    print("-> Bước 3: Dữ liệu sạch! Nạp vào Data Warehouse (Load)... ✅")
    return True

etl_pipeline_simulation(checkpoint_sql)
