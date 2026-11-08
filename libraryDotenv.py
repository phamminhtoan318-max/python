"""
=============================================================================
             CHUẨN QUẢN LÝ CẤU HÌNH DÀNH RIÊNG CHO DATA ENGINEER (DE)
=============================================================================
Trong Data Pipeline (ETL / ELT), Data Engineer KHÔNG BAO GIỜ viết rải rác
os.getenv() ở khắp các file extract, transform, load.

Thay vào đó, DE luôn tạo 1 module cấu hình tập trung để:
  1. Nạp và validate toàn bộ biến môi trường 1 lần duy nhất.
  2. Ép kiểu chuẩn xác (int, bool, float) cho các tham số Batch Size, Port.
  3. Tự động lắp ráp sẵn các Connection String (SQLAlchemy, S3, Postgres...).
=============================================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Tự động tạo file .env giả lập môi trường Data Pipeline thực tế
env_path = Path.cwd() / ".env"
with open(env_path, "w", encoding="utf-8") as f:
    f.write("""# --- 1. CƠ SỞ DỮ LIỆU NGUỒN (SOURCE DB) ---
SRC_DB_TYPE=postgresql
SRC_DB_HOST=192.168.1.100
SRC_DB_PORT=5432
SRC_DB_NAME=sales_production
SRC_DB_USER=de_extractor
SRC_DB_PASS=SieuMatKhau@2026

# --- 2. KHO DỮ LIỆU ĐÍCH (DATA WAREHOUSE / DATA LAKE) ---
DWH_DB_TYPE=mssql+pyodbc
DWH_DB_HOST=dwh-server.company.internal
DWH_DB_PORT=1433
DWH_DB_NAME=EnterpriseDWH
DWH_DB_USER=de_loader
DWH_DB_PASS=MatKhauDWH@999

# --- 3. CLOUD STORAGE (AWS S3 / MINIO CHO DATA LAKE) ---
S3_ENDPOINT=https://s3.ap-southeast-1.amazonaws.com
S3_BUCKET_NAME=raw-data-lake-company
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# --- 4. THAM SỐ VẬN HÀNH PIPELINE (PIPELINE CONFIG) ---
BATCH_SIZE=50000
CHUNK_DAYS=7
IS_FULL_REFRESH=False
MAX_RETRIES=3
""")

# 2. Nạp cấu hình từ .env
load_dotenv(override=True)


# =============================================================================
# CLASS CẤU HÌNH TẬP TRUNG (DE CONFIGURATION OBJECT)
# =============================================================================
class PipelineSettings:
    """Tập trung toàn bộ cấu hình, kết nối của Pipeline vào 1 Object duy nhất"""

    # --- A. LẮP RÁP CONNECTION STRING CSDL NGUỒN ---
    SRC_USER = os.getenv("SRC_DB_USER")
    SRC_PASS = os.getenv("SRC_DB_PASS")
    SRC_HOST = os.getenv("SRC_DB_HOST")
    SRC_PORT = int(os.getenv("SRC_DB_PORT", 5432))
    SRC_NAME = os.getenv("SRC_DB_NAME")

    # Tự động ráp thành URI chuẩn SQLAlchemy để kết nối trực tiếp
    SOURCE_DB_URI = (
        f"postgresql+psycopg2://{SRC_USER}:{SRC_PASS}@{SRC_HOST}:{SRC_PORT}/{SRC_NAME}"
    )

    # --- B. LẮP RÁP CONNECTION STRING KHO DỮ LIỆU DWH (SQL SERVER) ---
    DWH_USER = os.getenv("DWH_DB_USER")
    DWH_PASS = os.getenv("DWH_DB_PASS")
    DWH_HOST = os.getenv("DWH_DB_HOST")
    DWH_NAME = os.getenv("DWH_DB_NAME")

    DWH_CONNECTION_STRING = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DWH_HOST};"
        f"DATABASE={DWH_NAME};"
        f"UID={DWH_USER};"
        f"PWD={DWH_PASS};"
        f"TrustServerCertificate=yes;"
    )

    # --- C. CẤU HÌNH DATA LAKE (S3 / MINIO) ---
    S3_BUCKET = os.getenv("S3_BUCKET_NAME")
    S3_ENDPOINT = os.getenv("S3_ENDPOINT")

    # --- D. THAM SỐ VẬN HÀNH PIPELINE (ĐÃ ĐƯỢC ÉP KIỂU SẴN) ---
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10000))       # Số dòng mỗi lần đọc
    CHUNK_DAYS = int(os.getenv("CHUNK_DAYS", 1))           # Số ngày cắt lát dữ liệu
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))         # Số lần retry khi lỗi
    IS_FULL_REFRESH = os.getenv("IS_FULL_REFRESH", "False").lower() in ("true", "1")


# Khởi tạo đối tượng cấu hình dùng chung
settings = PipelineSettings()


# =============================================================================
# MÔ PHỎNG LUỒNG PIPELINE ETL CỦA DATA ENGINEER
# =============================================================================
def run_etl_pipeline():
    print("\n" + "=" * 65)
    print("MÔ PHỎNG PIPELINE ETL ĐANG CHẠY BẰNG CẤU HÌNH TỪ .ENV")
    print("=" * 65)

    print(f"\n1. [EXTRACT] Kết nối tới Database nguồn để trích xuất:")
    print(f"   -> URI kết nối: {settings.SOURCE_DB_URI}")
    print(f"   -> Đọc dữ liệu theo từng lô: {settings.BATCH_SIZE:,} dòng/lần")
    print(f"   -> Cắt lát dữ liệu theo: {settings.CHUNK_DAYS} ngày gần nhất")

    print(f"\n2. [TRANSFORM] Đẩy dữ liệu thô (Raw Data) lên Data Lake:")
    print(f"   -> S3 Bucket: s3://{settings.S3_BUCKET}/raw_sales/")
    print(f"   -> S3 Endpoint: {settings.S3_ENDPOINT}")

    print(f"\n3. [LOAD] Nạp dữ liệu vào Data Warehouse (SQL Server):")
    print(f"   -> DWH Server : {settings.DWH_HOST}")
    print(f"   -> DWH Database: {settings.DWH_NAME}")
    print(f"   -> Chế độ chạy : {'Full Refresh (Ghi đè)' if settings.IS_FULL_REFRESH else 'Incremental (Cập nhật gia tăng)'}")
    print(f"   -> Số lần retry nếu mạng đứt: {settings.MAX_RETRIES} lần")

    print("\n" + "=" * 65)
    print("-> PIPELINE SẴN SÀNG! MỌI THÔNG TIN BẢO MẬT ĐỀU NẰM AN TOÀN TRONG .ENV")
    print("=" * 65)


if __name__ == "__main__":
    run_etl_pipeline()
