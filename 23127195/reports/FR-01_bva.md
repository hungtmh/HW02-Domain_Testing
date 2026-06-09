# Boundary Value Analysis — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**Ngày:** 2026-06-09  
**SUT:** Frontend Web + API `POST /api/register`

---

## Bước 1 — Xác định các biên (Boundaries) từ đặc tả SRS

Dựa vào SRS FR-01, ta xác định các biên sau:

| B-ID | Biến | Ràng buộc SRS | Điểm biên dưới (Min) | Điểm biên trên (Max) | Kiểu biên |
|------|------|---------------|----------------------|----------------------|-----------|
| **B-PW-LEN** | password | Độ dài mật khẩu | 8 ký tự | Không giới hạn | Giá trị số |
| **B-PW-UP** | password | Số lượng chữ in hoa | 1 ký tự hoa | Không giới hạn | Số lượng thành phần |
| **B-PW-LO** | password | Số lượng chữ in thường | 1 ký tự thường | Không giới hạn | Số lượng thành phần |
| **B-PW-DI** | password | Số lượng chữ số | 1 chữ số | Không giới hạn | Số lượng thành phần |
| **B-PW-SP** | password | Số lượng ký tự đặc biệt | 1 ký tự đặc biệt (`@$!%*?&`) | Không giới hạn | Số lượng thành phần |
| **B-NAME-LEN** | name | Độ dài họ tên | 1 ký tự | Không giới hạn | Giá trị số |

---

## Bước 2 — Xác định các điểm kiểm thử biên (BVA Points)

Sử dụng phương pháp BVA truyền thống (chọn các điểm: Biên, Sát dưới biên, Sát trên biên) và Robustness testing (nếu cần).

### 1. Phân tích biên cho độ dài Mật khẩu (B-PW-LEN)
*Các thành phần cấu trúc khác được giữ đầy đủ và hợp lệ.*
- **Sát dưới biên (Min - 1):** 7 ký tự. Giá trị kiểm thử: `"Test12!"` -> Kỳ vọng: **Từ chối (Reject)**
- **Tại biên (Min):** 8 ký tự. Giá trị kiểm thử: `"Test123!"` -> Kỳ vọng: **Chấp nhận (Accept)**
- **Sát trên biên (Min + 1):** 9 ký tự. Giá trị kiểm thử: `"Test1234!"` -> Kỳ vọng: **Chấp nhận (Accept)**

### 2. Phân tích biên cho thành phần cấu trúc Mật khẩu (Password Composition)
*Giữ độ dài mật khẩu >= 8.*
- **Số chữ in hoa = 0 (Dưới biên):** `"test1234!"` -> Kỳ vọng: **Từ chối**
- **Số chữ in hoa = 1 (Tại biên):** `"Test1234!"` -> Kỳ vọng: **Chấp nhận**
- **Số chữ in thường = 0 (Dưới biên):** `"TEST1234!"` -> Kỳ vọng: **Từ chối**
- **Số chữ in thường = 1 (Tại biên):** `"tEST1234!"` -> Kỳ vọng: **Chấp nhận**
- **Số chữ số = 0 (Dưới biên):** `"TestTest!"` -> Kỳ vọng: **Từ chối**
- **Số chữ số = 1 (Tại biên):** `"Test1234!"` -> Kỳ vọng: **Chấp nhận**
- **Số ký tự đặc biệt = 0 (Dưới biên):** `"Test1234"` -> Kỳ vọng: **Từ chối**
- **Số ký tự đặc biệt = 1 (Tại biên):** `"Test1234!"` -> Kỳ vọng: **Chấp nhận**

### 3. Phân tích biên do cài đặt thực tế của mã nguồn (Implementation-specific boundary)
Do Regex kiểm tra mật khẩu ở Frontend Web bị lỗi (`(?=.*\s)` thay vì kiểm tra ký tự đặc biệt và giới hạn ký tự trong `[A-Za-z\d\s]`), chúng ta có biên cài đặt thực tế như sau:
- **Mật khẩu chứa ký tự đặc biệt chuẩn SRS, không chứa khoảng trắng:** `"Test1234!"` -> SRS: **Chấp nhận** | Frontend thực tế: **Từ chối**
- **Mật khẩu chứa khoảng trắng, không chứa ký tự đặc biệt SRS:** `"Test 1234"` -> SRS: **Từ chối** | Frontend thực tế: **Chấp nhận**

---

## Bước 3 — Danh sách Test Cases thiết kế từ BVA

*Mặc định: `name="Nguyen Van A"`, `email=<email duy nhất>` cho mỗi case.*

| TC-ID | Mật khẩu đầu vào | Vùng biên kiểm tra | Expected (SRS) | Expected (UI thực tế) | Expected (API thực tế) |
|-------|------------------|-------------------|----------------|-----------------------|------------------------|
| **BV-01** | `"Test12!"` (7 ký tự) | Độ dài Min - 1 | Từ chối | Từ chối | Từ chối |
| **BV-02** | `"Test123!"` (8 ký tự) | Độ dài Min | Chấp nhận | Từ chối (do lỗi regex) | Chấp nhận |
| **BV-03** | `"Test1234!"` (9 ký tự) | Độ dài Min + 1 | Chấp nhận | Từ chối (do lỗi regex) | Chấp nhận |
| **BV-04** | `"test1234!"` | Chữ in hoa = 0 | Từ chối | Từ chối | Từ chối |
| **BV-05** | `"TEST1234!"` | Chữ in thường = 0 | Từ chối | Từ chối | Từ chối |
| **BV-06** | `"TestTest!"` | Chữ số = 0 | Từ chối | Từ chối | Từ chối |
| **BV-07** | `"Test1234"` | Ký tự đặc biệt = 0 | Từ chối | Từ chối | Từ chối |
| **BV-08** | `"Test 1234"` | Chứa khoảng trắng, không có special SRS | Từ chối | Chấp nhận | Chấp nhận (do backend không validate) |
| **BV-09** | `name="A"` (1 ký tự) | Độ dài name Min | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-10** | `name=""` (0 ký tự) | Độ dài name Min - 1 | Từ chối | Chặn submit (HTML5 `required`) | Từ chối |
| **BV-11** | `email="a@b.co"` (TLD 2 ký tự) | Biên định dạng email ngắn nhất | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-12** | `email="a@b.c"` (TLD 1 ký tự) | Biên định dạng email không hợp lệ | Từ chối | Từ chối | Từ chối |

---

## Bước 4 — Kịch bản biên Robustness / Edge cases bổ sung

| TC-ID | Đầu vào kiểm thử | Mục đích kiểm tra | Kết quả mong đợi |
|-------|------------------|-------------------|------------------|
| **BV-R01** | password dài 500 ký tự | Kiểm tra tràn bộ đệm / giới hạn đầu vào | Từ chối hoặc chấp nhận an toàn, không crash hệ thống |
| **BV-R02** | name có ký tự Unicode `"Nguyễn Văn Hoài"` | Kiểm tra hỗ trợ đa ngôn ngữ | Chấp nhận đăng ký |
| **BV-R03** | email có phần domain in hoa `"user@TEST.COM"` | Kiểm tra tính không phân biệt hoa thường của domain | Chấp nhận đăng ký |
