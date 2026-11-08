"""
=============================================================================
             CẨM NANG TOÀN DIỆN VỀ CƠ SỞ DỮ LIỆU TRONG PYTHON
=============================================================================
1. pyodbc (Database Driver):
   Động cơ bên dưới, kết nối trực tiếp với CSDL (đặc biệt là Microsoft SQL Server)
   qua cổng ODBC của hệ điều hành. Viết bằng câu lệnh SQL thô.

2. SQLAlchemy (ORM & SQL Toolkit):
   Vô-lăng & Bảng điều khiển cao cấp. Thao tác CSDL thông qua Class và Object
   của Python, không cần viết SQL thô, độc lập hệ quản trị CSDL.

Quy trình gốc của mọi thư viện DB:
   Connect (Kết nối) -> Cursor (Con trỏ) -> Execute (Chạy lệnh) -> Commit (Lưu)
=============================================================================
"""

# =============================================================================
# CHẶNG 1: BẢN CHẤT CƠ SỞ DỮ LIỆU QUA THƯ VIỆN CÓ SẴN (SQLITE3)
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 1: BẢN CHẤT NGUYÊN THỦY CỦA DATABASE (SQLITE3)")
print("=" * 60)

import sqlite3

# 1. Kết nối tới file CSDL (tự tạo ra 'database.db' nếu chưa có)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 2. Tạo bảng bằng câu lệnh SQL thô
cursor.execute("""
CREATE TABLE IF NOT EXISTS nguoi_dung (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL,
    email TEXT UNIQUE
)
""")

# 3. Thêm dữ liệu (INSERT) - Dùng '?' để chống hack SQL Injection
cursor.execute(
    "INSERT OR IGNORE INTO nguoi_dung (ten, email) VALUES (?, ?)",
    ("Toan Pham", "toan@gmail.com")
)
conn.commit()  # BẮT BUỘC có commit() để lưu dữ liệu xuống đĩa cứng

# 4. Lấy dữ liệu (SELECT)
cursor.execute("SELECT id, ten, email FROM nguoi_dung")
users = cursor.fetchall()
print("Dữ liệu bảng 'nguoi_dung' qua sqlite3:")
for u in users:
    print(f"  ID: {u[0]} | Tên: {u[1]} | Email: {u[2]}")

# 5. Đóng kết nối
conn.close()


# =============================================================================
# CHẶNG 2: SQLALCHEMY 2.0 – ĐỊNH NGHĨA BẢNG BẰNG CLASS PYTHON (MODEL)
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 2: SQLALCHEMY 2.0 – ĐỊNH NGHĨA BẢNG BẰNG CLASS (MODEL)")
print("=" * 60)

from sqlalchemy import create_engine, String, Float, select, desc, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# 1. Khởi tạo Engine (đường ống kết nối tới file 'cua_hang.db')
engine = create_engine("sqlite:///cua_hang.db", echo=False)

# 2. Base Class dùng cho việc kế thừa mô hình bảng
class Base(DeclarativeBase):
    pass

# 3. Định nghĩa bảng 'san_pham' (Mỗi thuộc tính đại diện cho một cột)
class SanPham(Base):
    __tablename__ = "san_pham"

    id: Mapped[int] = mapped_column(primary_key=True)       # Khóa chính tự tăng
    ten: Mapped[str] = mapped_column(String(100))           # Chuỗi ký tự
    gia: Mapped[float] = mapped_column(Float)               # Số thực
    so_luong: Mapped[int] = mapped_column(default=0)        # Mặc định = 0

    def __repr__(self):
        return f"<SanPham(id={self.id}, ten='{self.ten}', gia={self.gia}$, sl={self.so_luong})>"

# 4. Tạo mới hoặc làm mới bảng trong CSDL
Base.metadata.drop_all(engine)    # Reset dữ liệu cũ để mỗi lần chạy đều sạch sẽ
Base.metadata.create_all(engine)  # Tự động sinh bảng 'san_pham'
print("-> Đã khởi tạo bảng 'san_pham' thành công qua SQLAlchemy!")


# =============================================================================
# CHẶNG 3: THAO TÁC C.R.U.D HOÀN CHỈNH VỚI SESSION
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 3: TRỌN BỘ 4 THAO TÁC C.R.U.D VỚI SESSION")
print("=" * 60)

with Session(engine) as session:
    # -------------------------------------------------------------------------
    # 1. CREATE (Thêm mới dữ liệu)
    # -------------------------------------------------------------------------
    sp1 = SanPham(ten="Bàn phím cơ", gia=85.0, so_luong=10)
    sp2 = SanPham(ten="Chuột Gaming", gia=45.0, so_luong=25)
    sp3 = SanPham(ten="Tai nghe Bluetooth", gia=120.0, so_luong=5)

    session.add_all([sp1, sp2, sp3])
    session.commit()  # Xác nhận lưu vào Database
    print("1. [CREATE] Đã thêm thành công 3 sản phẩm vào CSDL.")

    # -------------------------------------------------------------------------
    # 2. READ (Đọc dữ liệu)
    # -------------------------------------------------------------------------
    # Lấy nhanh theo ID bằng session.get()
    sp_id_1 = session.get(SanPham, 1)
    print(f"2. [READ theo ID=1]: {sp_id_1}")

    # Lấy toàn bộ danh sách bằng select()
    query_all = select(SanPham)
    danh_sach = session.scalars(query_all).all()
    print(f"   [READ toàn bộ]: Có tổng cộng {len(danh_sach)} sản phẩm trong kho.")

    # -------------------------------------------------------------------------
    # 3. UPDATE (Cập nhật dữ liệu)
    # -------------------------------------------------------------------------
    # Chỉ cần đổi trực tiếp giá trị thuộc tính của object, SQLAlchemy tự UPDATE!
    if sp_id_1:
        sp_id_1.gia = 79.99   # Giảm giá
        session.commit()      # Lưu thay đổi
        print(f"3. [UPDATE] Đã cập nhật giá mới cho ID=1: {sp_id_1.gia}$")

    # -------------------------------------------------------------------------
    # 4. DELETE (Xóa dữ liệu)
    # -------------------------------------------------------------------------
    # Ví dụ xóa sản phẩm:
    # session.delete(sp_id_1)
    # session.commit()
    print("4. [DELETE] Cú pháp: session.delete(object) -> session.commit()")


# =============================================================================
# CHẶNG 4: TRUY VẤN & LỌC NÂNG CAO (WHERE, ORDER_BY, LIMIT)
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 4: TRUY VẤN & LỌC NÂNG CAO")
print("=" * 60)

with Session(engine) as session:
    # Lấy sản phẩm có giá > 50$, sắp xếp GIẢM DẦN theo giá, lấy tối đa 2 món
    query_top = (
        select(SanPham)
        .where(SanPham.gia > 50.0)
        .order_by(desc(SanPham.gia))
        .limit(2)
    )
    top_sp = session.scalars(query_top).all()
    print("Top sản phẩm giá cao (> 50$):")
    for sp in top_sp:
        print(f"  * {sp.ten}: {sp.gia}$ (Kho còn: {sp.so_luong})")

    # Tìm kiếm theo chuỗi con (tương đương LIKE '%Gaming%' trong SQL)
    query_search = select(SanPham).where(SanPham.ten.contains("Gaming"))
    sp_gaming = session.scalars(query_search).first()
    print(f"\nTìm kiếm sản phẩm chứa từ 'Gaming': {sp_gaming}")


# =============================================================================
# CHẶNG 5: CHẠY RAW SQL VÀ KẾT NỐI SANG SQL SERVER QUA PYODBC
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 5: RAW SQL AN TOÀN & CÔNG THỨC KẾT NỐI SQL SERVER")
print("=" * 60)

# 1. Chạy Raw SQL an toàn với hàm text() trong SQLAlchemy
with Session(engine) as session:
    sql_raw = text("SELECT ten, gia FROM san_pham WHERE gia < :muc_gia")
    ket_qua = session.execute(sql_raw, {"muc_gia": 100.0})
    print("Kết quả chạy Raw SQL (sản phẩm < 100$):")
    for row in ket_qua:
        print(f"  * Tên: {row.ten:<20} | Giá: {row.gia}$")

# 2. CÔNG THỨC CHUYỂN SANG MICROSOFT SQL SERVER QUA PYODBC:
print("""
Mẹo thực tế khi làm việc với Microsoft SQL Server:
Bạn CHỈ CẦN THAY duy nhất 1 dòng create_engine() ở đầu file:

engine = create_engine(
    "mssql+pyodbc://sa:MatKhau123@localhost:1433/TenDatabase"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

Toàn bộ Model, truy vấn select(), CRUD ở các Chặng 2, 3, 4 bên trên
hoàn toàn GIỮ NGUYÊN 100%, không cần phải sửa bất kỳ dòng code nào!
""")



