"""
=============================================================================
         CẨM NANG TOÀN DIỆN THƯ VIỆN REQUESTS DÀNH CHO DATA ENGINEER (DE)
=============================================================================
Được chia thành 10 Chặng độc lập tương ứng trọn vẹn 10 tiêu chuẩn công nghiệp:
  Chặng 1 : HTTP Method - GET (Trích xuất dữ liệu cơ bản)
  Chặng 2 : Query Parameters (Lọc dữ liệu an toàn với params=)
  Chặng 3 : Request Body (Phân biệt json=, data=, files= khi gửi đi)
  Chặng 4 : Response Parsing (Phân biệt .json(), .text, .content)
  Chặng 5 : Exception Handling (Bắt 4 loại lỗi: Timeout, Connection, HTTP, JSON)
  Chặng 6 : Rate Limit (Bắt HTTP 429 & đọc Header Retry-After để tạm dừng)
  Chặng 7 : Idempotency khi Retry (Dùng Idempotency-Key chống trùng lặp dữ liệu)
  Chặng 8 : Incremental Extraction (Kéo dữ liệu gia tăng qua mốc Watermark)
  Chặng 9 : Logging & Monitoring (Ghi nhận latency, status, số bản ghi)
  Chặng 10: API Security (Bảo mật Token qua .env & kiểm tra chứng chỉ SSL)
=============================================================================
"""

import os
import time
import uuid
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

# Nạp file cấu hình môi trường
load_dotenv()


# =============================================================================
# CHẶNG 1: HTTP METHOD – GET (TRÍCH XUẤT DỮ LIỆU CƠ BẢN)
# =============================================================================
# 💣 Nếu không có: Bất lực, không thể lấy dữ liệu từ bên thứ 3 (Shopee, Stripe...).
# 🛡️ DE dùng để: Bước Extract (E) khởi đầu kéo dữ liệu về máy chủ công ty.
print("\n" + "=" * 65)
print("CHẶNG 1: HTTP METHOD – GET (TRÍCH XUẤT DỮ LIỆU)")
print("=" * 65)

url_get = "https://jsonplaceholder.typicode.com/posts/1"
res_get = requests.get(url_get, timeout=10)

print(f"Mã trạng thái HTTP : {res_get.status_code}")
print(f"Dữ liệu trích xuất : {res_get.json().get('title')[:40]}...")


# =============================================================================
# CHẶNG 2: QUERY PARAMETERS (LỌC DỮ LIỆU AN TOÀN VỚI PARAMS=)
# =============================================================================
# 💣 Nếu không có: Nối chuỗi thủ công gây lỗi khi có dấu cách, ký tự tiếng Việt.
# 🛡️ DE dùng để: Lọc dữ liệu theo ngày, trạng thái, phân trang một cách an toàn.
print("\n" + "=" * 65)
print("CHẶNG 2: QUERY PARAMETERS (PARAMS=)")
print("=" * 65)

query_params = {
    "postId": 1,
    "_limit": 3
}
# requests tự động lắp ráp thành: .../comments?postId=1&_limit=3
res_params = requests.get(
    "https://jsonplaceholder.typicode.com/comments",
    params=query_params,
    timeout=10
)
print(f"URL hoàn chỉnh tự động ráp: {res_params.url}")
print(f"Số bản ghi lọc được      : {len(res_params.json())} bình luận")


# =============================================================================
# CHẶNG 3: REQUEST BODY – PHÂN BIỆT JSON=, DATA= VÀ FILES=
# =============================================================================
# 💣 Nếu không có: Gửi sai định dạng bị lỗi 415/400; không upload được file CSV.
# 🛡️ DE dùng để: Gửi JSON cho REST API, gửi Form, và upload file lên kho đối tác.
print("\n" + "=" * 65)
print("CHẶNG 3: REQUEST BODY (JSON=, DATA=, FILES=)")
print("=" * 65)

# 1. json=: Gửi dữ liệu có cấu trúc REST API
payload_json = {"pipeline_id": "ETL_01", "rows": 1000}
r_json = requests.post("https://httpbin.org/post", json=payload_json, timeout=10)
print("1. [json=]  Server nhận JSON:", r_json.json()["json"])

# 2. data=: Gửi dữ liệu dạng Form web (x-www-form-urlencoded)
payload_form = {"grant_type": "client_credentials"}
r_data = requests.post("https://httpbin.org/post", data=payload_form, timeout=10)
print("2. [data=]  Server nhận Form:", r_data.json()["form"])

# 3. files=: Upload tệp tin dữ liệu (CSV/Parquet) lên máy chủ
temp_csv = Path("sample_data.csv")
temp_csv.write_text("id,val\n1,100\n", encoding="utf-8")
with open(temp_csv, "rb") as f:
    r_files = requests.post("https://httpbin.org/post", files={"file_data": f}, timeout=10)
    print("3. [files=] Đã upload file  :", list(r_files.json()["files"].keys()))


# =============================================================================
# CHẶNG 4: RESPONSE PARSING – PHÂN BIỆT .JSON(), .TEXT, .CONTENT
# =============================================================================
# 💣 Nếu không có: Lấy nhầm .text lưu ảnh/zip sẽ làm hỏng file; dùng .content cho bảng thì không đọc được trường.
# 🛡️ DE dùng để: Lấy đúng định dạng dữ liệu (Dict, Text String, hoặc Raw Bytes).
print("\n" + "=" * 65)
print("CHẶNG 4: RESPONSE PARSING (.JSON(), .TEXT, .CONTENT)")
print("=" * 65)

res_parse = requests.get("https://httpbin.org/get", timeout=10)

print(f"1. .json()  (Dictionary) : {type(res_parse.json())} -> Lấy trường: {res_parse.json()['url']}")
print(f"2. .text    (Unicode Str) : {type(res_parse.text)} -> Độ dài chuỗi: {len(res_parse.text)} ký tự")
print(f"3. .content (Raw Bytes)   : {type(res_parse.content)} -> Kích thước: {len(res_parse.content)} bytes (dùng lưu file nhị phân)")


# =============================================================================
# CHẶNG 5: EXCEPTION HANDLING (XỬ LÝ 4 LOẠI LỖI MẠNG KINH ĐIỂN)
# =============================================================================
# 💣 Nếu không có: Pipeline chạy đêm gặp mạng giật hoặc lỗi 502 HTML sẽ sập toàn bộ hệ thống.
# 🛡️ DE dùng để: Bắt trọn 4 lỗi mạng, ghi log và kết thúc an toàn mà không bị crash.
print("\n" + "=" * 65)
print("CHẶNG 5: EXCEPTION HANDLING (TIMEOUT, HTTP, CONNECTION, JSON)")
print("=" * 65)

def safe_call(url: str):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()  # Ném lỗi HTTPError nếu mã >= 400
        return r.json()       # Ném lỗi JSONDecodeError nếu server trả về HTML lỗi
    except requests.exceptions.Timeout:
        print(f"-> [Lỗi] Quá thời gian chờ (Timeout) tại: {url}")
    except requests.exceptions.ConnectionError:
        print(f"-> [Lỗi] Không thể kết nối mạng (ConnectionError) tới: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"-> [Lỗi] Máy chủ phản hồi mã lỗi HTTP: {e.response.status_code}")
    except requests.exceptions.JSONDecodeError:
        print("-> [Lỗi] Server trả về HTML/chữ thô thay vì định dạng JSON!")
    except requests.exceptions.RequestException as e:
        print(f"-> [Lỗi khác]: {e}")
    return None

# Test link thành công và link lỗi 404:
_ = safe_call("https://jsonplaceholder.typicode.com/posts/1")
_ = safe_call("https://httpbin.org/status/404")


# =============================================================================
# CHẶNG 6: RATE LIMIT (HTTP 429 & HEADER RETRY-AFTER)
# =============================================================================
# 💣 Nếu không có: Gọi quá nhanh bị đối tác khóa IP (Blacklist) vĩnh viễn vì nghi tấn công DDoS.
# 🛡️ DE dùng để: Tự động tạm dừng đúng số giây đối tác yêu cầu trước khi tiếp tục kéo data.
print("\n" + "=" * 65)
print("CHẶNG 6: RATE LIMIT (429) & HEADER RETRY-AFTER")
print("=" * 65)

def call_with_rate_limit(url: str):
    res = requests.get(url, timeout=5)
    if res.status_code == 429:
        # Đọc Header Retry-After từ đối tác (mặc định ngủ 3s nếu server không gửi)
        wait_seconds = int(res.headers.get("Retry-After", 3))
        print(f"-> [Cảnh báo 429] Bị giới hạn tốc độ! Tạm dừng {wait_seconds}s...")
        time.sleep(wait_seconds)
        return requests.get(url, timeout=5)
    print(f"Gọi API bình thường, mã trạng thái: {res.status_code}")
    return res

_ = call_with_rate_limit("https://httpbin.org/get")


# =============================================================================
# CHẶNG 7: IDEMPOTENCY KHI RETRY (CHỐNG TRÙNG LẶP DỮ LIỆU)
# =============================================================================
# 💣 Nếu không có: Mạng lag gửi lại request POST làm trừ tiền 2 lần hoặc tạo trùng bản ghi.
# 🛡️ DE dùng để: Gửi mã UUID duy nhất để server đối tác chỉ thực thi đúng 1 lần duy nhất dù có retry.
print("\n" + "=" * 65)
print("CHẶNG 7: IDEMPOTENCY KHI RETRY (UUID TOKEN)")
print("=" * 65)

# Sinh một mã Idempotency duy nhất cho phiên chạy này
idempotency_key = str(uuid.uuid4())
headers_idem = {
    "Idempotency-Key": idempotency_key,
    "Content-Type": "application/json"
}

res_idem = requests.post(
    "https://httpbin.org/post",
    json={"order_id": 9999, "amount": 250.0},
    headers=headers_idem,
    timeout=5
)
print(f"Mã Idempotency-Key sinh ra : {idempotency_key}")
print(f"Server xác nhận khóa đã nhận : {res_idem.json()['headers'].get('Idempotency-Key')}")


# =============================================================================
# CHẶNG 8: INCREMENTAL EXTRACTION (WATERMARK / UPDATED_SINCE)
# =============================================================================
# 💣 Nếu không có: Mỗi đêm phải kéo lại 10 năm dữ liệu (tốn hàng ngàn USD băng thông & giờ chạy).
# 🛡️ DE dùng để: Chỉ kéo đúng các dòng mới phát sinh kể từ mốc chạy cuối cùng (Last Watermark).
print("\n" + "=" * 65)
print("CHẶNG 8: INCREMENTAL EXTRACTION (WATERMARK)")
print("=" * 65)

# Lưu mốc thời gian lần chạy cuối cùng vào Database hoặc File:
last_watermark = "2026-11-07T00:00:00Z"

params_incremental = {
    "updated_since": last_watermark,
    "status": "COMPLETED",
    "_limit": 3
}

res_inc = requests.get(
    "https://jsonplaceholder.typicode.com/comments",
    params=params_incremental,
    timeout=10
)
print(f"Kéo dữ liệu với Watermark: updated_since >= {last_watermark}")
print(f"Số bản ghi mới trích xuất : {len(res_inc.json())} dòng")


# =============================================================================
# CHẶNG 9: LOGGING & MONITORING GIÁM SÁT PIPELINE
# =============================================================================
# 💣 Nếu không có: Mất dữ liệu không rõ nguyên nhân, không biết API chậm ở khâu nào.
# 🛡️ DE dùng để: Ghi "hộp đen" theo dõi: URL, thời gian phản hồi, số dòng kéo được.
print("\n" + "=" * 65)
print("CHẶNG 9: LOGGING & MONITORING PIPELINE")
print("=" * 65)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("DE_Monitor")

start_time = time.time()
res_mon = requests.get("https://jsonplaceholder.typicode.com/posts?_limit=5", timeout=5)
elapsed = time.time() - start_time
records_count = len(res_mon.json())

# Ghi nhận giám sát hệ thống chuẩn DE:
logger.info(
    f"Trích xuất thành công | Status: {res_mon.status_code} | "
    f"Thời gian: {elapsed:.3f}s | Số bản ghi: {records_count} dòng"
)


# =============================================================================
# CHẶNG 10: API SECURITY (TOKEN .ENV, HTTPS & SSL VERIFICATION)
# =============================================================================
# 💣 Nếu không có: Lộ token trên GitHub bị cướp tài khoản; gọi server nội bộ bị lỗi SSLError chặn kết nối.
# 🛡️ DE dùng để: Giấu kín token trong .env và kiểm soát chứng chỉ bảo mật SSL (verify=True/False).
print("\n" + "=" * 65)
print("CHẶNG 10: API SECURITY (TOKEN .ENV & SSL VERIFY)")
print("=" * 65)

# Lấy token an toàn từ .env (không bao giờ viết cứng vào code)
secret_token = os.getenv("API_KEY", "default_secret_token")

secure_headers = {
    "Authorization": f"Bearer {secret_token}",
    "User-Agent": "SecureDataPipeline/1.0"
}

# verify=True: Bật kiểm tra chứng chỉ bảo mật HTTPS (chuẩn an toàn)
# verify=False: Dùng khi kết nối mạng nội bộ công ty có chứng chỉ tự ký (Self-signed cert)
res_sec = requests.get(
    "https://httpbin.org/get",
    headers=secure_headers,
    timeout=5,
    verify=True
)

print(f"Token bảo mật đọc từ .env : {secret_token[:7]}***** (Được ẩn an toàn)")
print(f"Kết nối HTTPS + SSL xác thực: {'Thành công' if res_sec.status_code == 200 else 'Thất bại'}")

print("\n" + "=" * 65)
print("HOÀN TẤT 100% CẢ 10 CHẶNG REQUESTS THỰC CHIẾN DÀNH CHO DATA ENGINEER!")
print("=" * 65)
