"""
=============================================================================
             CẨM NANG CHUYÊN SÂU TỪ A ĐẾN Z VỀ MODULE DATETIME
=============================================================================
Module datetime trong Python bao gồm 5 lớp cốt lõi:
  1. date       : Chỉ chứa Năm, Tháng, Ngày (Không có giờ)
  2. time       : Chỉ chứa Giờ, Phút, Giây, Microgiây (Không có ngày)
  3. datetime   : Kết hợp cả date và time (Dùng nhiều nhất ~90%)
  4. timedelta  : Khoảng thời gian / Độ lệch (Dùng để cộng, trừ thời gian)
  5. timezone   : Xử lý múi giờ (UTC, Asia/Ho_Chi_Minh...)
=============================================================================
"""

from datetime import datetime, date, time, timedelta, timezone
from zoneinfo import ZoneInfo  # Thư viện chuẩn từ Python 3.9+ để xử lý múi giờ địa lý


# =============================================================================
# CHẶNG 1: KHỞI TẠO VÀ BÓC TÁCH CÁC THÀNH PHẦN (EXTRACT ATTRIBUTES)
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 1: KHỞI TẠO VÀ TRÍCH XUẤT THÀNH PHẦN")
print("=" * 60)

# 1. Khởi tạo ngày giờ hiện tại
now = datetime.now()
today = date.today()

print("datetime.now():", now)
print("date.today()  :", today)

# 2. Khởi tạo thủ công mốc thời gian cụ thể (Năm, Tháng, Ngày, Giờ, Phút, Giây)
my_birthday = datetime(2003, 10, 15, 8, 30, 0)
print("Ngày sinh cụ thể:", my_birthday)

# 3. Trích xuất từng thành phần từ đối tượng datetime
print("\nTrích xuất từng thông số của 'now':")
print(f"  * Năm: {now.year}")
print(f"  * Tháng: {now.month}")
print(f"  * Ngày: {now.day}")
print(f"  * Giờ: {now.hour}")
print(f"  * Phút: {now.minute}")
print(f"  * Giây: {now.second}")
print(f"  * Microgiây: {now.microsecond}")

# 4. Thứ trong tuần (Weekday): 0 = Thứ Hai, ..., 6 = Chủ Nhật
thu_trong_tuan = now.weekday()
ten_thu = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
print(f"  * Thứ trong tuần: {ten_thu[thu_trong_tuan]} (weekday index: {thu_trong_tuan})")


# =============================================================================
# CHẶNG 2: TÍNH TOÁN THỜI GIAN VỚI TIMEDELTA (CỘNG / TRỪ THỜI GIAN)
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 2: TÍNH TOÁN THỜI GIAN VỚI TIMEDELTA")
print("=" * 60)

# timedelta nhận các tham số: days, seconds, microseconds, milliseconds, minutes, hours, weeks
# Lưu ý: timedelta KHÔNG nhận 'months' hay 'years' vì số ngày của tháng/năm không cố định!

hien_tai = datetime.now()

# 1. Cộng / Trừ mốc thời gian
sau_7_ngay = hien_tai + timedelta(days=7)
truoc_3_tieng = hien_tai - timedelta(hours=3)
het_han_token = hien_tai + timedelta(minutes=45, seconds=30)

print(f"Hiện tại             : {hien_tai.strftime('%d/%m/%Y %H:%M')}")
print(f"Sau 7 ngày nữa       : {sau_7_ngay.strftime('%d/%m/%Y %H:%M')}")
print(f"Trước đây 3 tiếng    : {truoc_3_tieng.strftime('%d/%m/%Y %H:%M')}")
print(f"Token hết hạn sau 45p: {het_han_token.strftime('%d/%m/%Y %H:%M:%S')}")

# 2. Tính khoảng cách giữa 2 mốc thời gian (dt2 - dt1 -> timedelta object)
tet_duong_lich = datetime(2027, 1, 1, 0, 0, 0)
khoang_cach = tet_duong_lich - hien_tai

print(f"\nĐếm ngược tới Tết Dương Lịch 2027:")
print(f"  * Số ngày còn lại   : {khoang_cach.days} ngày")
print(f"  * Tổng số giây còn  : {int(khoang_cach.total_seconds()):,} giây")
print(f"  * Tổng số giờ quy đổi: {khoang_cach.total_seconds() / 3600:.1f} giờ")


# =============================================================================
# CHẶNG 3: ĐỊNH DẠNG (STRFTIME) & ÉP CHUỖI (STRPTIME)
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 3: STRFTIME (ĐỐI TƯỢNG -> CHUỖI) & STRPTIME (CHUỖI -> ĐỐI TƯỢNG)")
print("=" * 60)

# MẸO NHỚ:
#   * strftime = String Format Time (Biến datetime thành String để in)
#   * strptime = String Parse Time  (Phân tích String thành datetime để tính)

dt_sample = datetime(2026, 11, 8, 16, 45, 30)

# 1. STRFTIME: Định dạng các kiểu hiển thị
print("Định dạng chuẩn Việt Nam   :", dt_sample.strftime("%d/%m/%Y %H:%M:%S"))
print("Định dạng chuẩn Quốc tế/ISO:", dt_sample.strftime("%Y-%m-%d %H:%M:%S"))
print("Định dạng 12 giờ có AM/PM  :", dt_sample.strftime("%I:%M:%S %p"))
print("Tên thứ và tháng bằng chữ   :", dt_sample.strftime("%A, ngày %d tháng %B năm %Y"))

# 2. STRPTIME: Chuyển dữ liệu người dùng nhập hoặc chuỗi từ API về Datetime
chuoi_ngay_api = "2026-12-31T23:59:59"
dt_parsed = datetime.strptime(chuoi_ngay_api, "%Y-%m-%dT%H:%M:%S")
print("\nChuỗi ban đầu:", chuoi_ngay_api)
print("Đã parse thành đối tượng:", dt_parsed, "| Kiểu:", type(dt_parsed))

chuoi_viet_nam = "25/12/2026 08:30"
dt_vn = datetime.strptime(chuoi_viet_nam, "%d/%m/%Y %H:%M")
print("Parse chuỗi VN thành công:", dt_vn)


# =============================================================================
# CHẶNG 4: UNIX TIMESTAMP (KỶ NGUYÊN EPOCH - 1970)
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 4: UNIX TIMESTAMP (SỐ GIÂY KỂ TỪ 01/01/1970 UTC)")
print("=" * 60)

# Tại sao Database và API hay dùng Timestamp?
# Vì Timestamp là 1 con số nguyên (Float/Int), lưu trữ siêu nhẹ và không bị dính lỗi định dạng chuỗi!

# 1. Chuyển datetime hiện tại thành Unix Timestamp (.timestamp())
timestamp_now = now.timestamp()
print("Unix Timestamp hiện tại:", timestamp_now)  # vd: 1794130000.123

# 2. Đổi từ Unix Timestamp ngược lại thành đối tượng datetime (.fromtimestamp())
dt_from_ts = datetime.fromtimestamp(timestamp_now)
print("Chuyển ngược lại Datetime:", dt_from_ts)

# 3. Đổi số 0 thành thời gian mốc lịch sử Epoch (theo giờ địa phương)
print("Mốc thời gian số 0 (Epoch):", datetime.fromtimestamp(0))


# =============================================================================
# CHẶNG 5: MÚI GIỜ (TIMEZONE) – NAIVE VS AWARE DATETIME
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 5: MÚI GIỜ CHUẨN QUỐC TẾ (NAIVE VS AWARE DATETIME)")
print("=" * 60)

# BẪY KINH ĐIỂN:
#   * Naive Datetime: Không có thông tin múi giờ (mặc định của datetime.now())
#   * Aware Datetime: Có gắn kèm múi giờ (UTC hoặc Zone cụ thể)

# 1. Lấy giờ chuẩn quốc tế UTC (Aware Datetime)
utc_now = datetime.now(timezone.utc)
print("Giờ UTC chuẩn quốc tế       :", utc_now)

# 2. Chuyển đổi múi giờ sang giờ Việt Nam (Asia/Ho_Chi_Minh - UTC+7) bằng zoneinfo
vietnam_tz = ZoneInfo("Asia/Ho_Chi_Minh")
vn_time = utc_now.astimezone(vietnam_tz)
print("Giờ Việt Nam (Asia/Ho_Chi_Minh):", vn_time)

# 3. Chuyển đổi sang giờ Tokyo (Nhật Bản - UTC+9) và New York (Mỹ - UTC-5)
tokyo_tz = ZoneInfo("Asia/Tokyo")
ny_tz = ZoneInfo("America/New_York")

tokyo_time = utc_now.astimezone(tokyo_tz)
ny_time = utc_now.astimezone(ny_tz)

print("Cùng thời điểm đó tại Tokyo    :", tokyo_time.strftime("%H:%M:%S (%Z)"))
print("Cùng thời điểm đó tại New York :", ny_time.strftime("%H:%M:%S (%Z)"))


# =============================================================================
# CHẶNG 6: BẢNG TRA CỨU CÁC KÝ HIỆU FORMAT ĐẶC TẢ THÔNG DỤNG NHẤT
# =============================================================================
print("\n" + "=" * 60)
print("CHẶNG 6: BẢNG KÝ TỰ FORMAT CẦN THUỘC LÒNG")
print("=" * 60)
print("""
  %Y : Năm 4 chữ số (2026)      | %y : Năm 2 chữ số cuối (26)
  %m : Tháng dạng số 01-12      | %B : Tên tháng đầy đủ (November)
  %d : Ngày trong tháng 01-31   | %A : Tên thứ đầy đủ (Sunday, Monday)
  %H : Giờ dạng 24h (00-23)     | %I : Giờ dạng 12h (01-12)
  %M : Phút (00-59)             | %S : Giây (00-59)
  %p : AM hoặc PM               | %f : Microgiây (000000 - 999999)
  %Z : Tên múi giờ (vd: UTC, ICT, JST)
""")
