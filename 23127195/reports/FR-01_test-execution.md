# Test Execution — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**Ngày thực thi:** 2026-06-09  
**Môi trường thử nghiệm:** Windows 10, Node.js v18+, SQLite, Chrome / React Web (:5173)  
**Người thực hiện:** 23127195  

---

## 1. Kết quả tổng hợp (Test Summary)

| Chỉ số (Metric) | Số lượng (Count) |
|-----------------|------------------|
| Tổng số test case thiết kế | 17 |
| Đã thực thi (Executed) | 15 |
| **ĐẠT (Pass)** | 4 |
| **KHÔNG ĐẠT (Fail)** | 11 |
| Chưa chạy (Not run) | 2 |

---

## 2. Nhật ký thực thi API Layer (`POST /api/register`)

Thực hiện gọi API trực tiếp bằng PowerShell `Invoke-RestMethod` để kiểm tra khả năng kiểm thực ở phía server (Backend validation bypass):

| TC-ID | Dữ liệu đầu vào (Request Body) | HTTP Code | Kết quả thực tế (Actual) | Kết quả mong đợi (Expected) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-----------------------------|-----------|--------------------------|----------------------------|---------------------|-----------------|
| **DT-01** | `name="Nguyen Van A"`, `email="new_auth_01@test.com"`, `password="Test1234!"` | 200 OK | `{"message":"User registered successfully","id":3}` | Đăng ký thành công, tạo tài khoản mới | **PASS** | — |
| **DT-02** | `email="test@eshop.com"` (Đã có sẵn trong DB) | 200 OK | `{"message":"User registered successfully","id":4}` | Từ chối đăng ký, báo trùng email | **FAIL** | [BUG-001](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-001.md) |
| **DT-03** | `email="invalid-email"` | 200 OK | `{"message":"User registered successfully","id":5}` | Từ chối đăng ký, báo sai định dạng | **FAIL** | [BUG-002](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-002.md) |
| **DT-04** | `email=""` (Bỏ trống email) | 200 OK | `{"message":"User registered successfully","id":6}` | Từ chối đăng ký | **FAIL** | [BUG-003](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-003.md) |
| **DT-05** | `name=""` (Bỏ trống họ tên) | 200 OK | `{"message":"User registered successfully","id":6}` | Từ chối đăng ký | **FAIL** | [BUG-003](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-003.md) |
| **BV-01** | `password="Test12!"` (7 ký tự) | 200 OK | `{"message":"User registered successfully","id":7}` | Từ chối đăng ký | **FAIL** | [BUG-004](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-004.md) |
| **BV-02** | `password="Test123!"` (8 ký tự) | 200 OK | `{"message":"User registered successfully","id":8}` | Chấp nhận đăng ký | **PASS** | — |
| **BV-04** | `password="test1234!"` (Thiếu chữ hoa) | 200 OK | `{"message":"User registered successfully","id":8}` | Từ chối đăng ký | **FAIL** | [BUG-004](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-004.md) |
| **BV-08** | `password="Test 1234"` (Có space, không special) | 200 OK | `{"message":"User registered successfully","id":9}` | Từ chối đăng ký | **FAIL** | [BUG-004](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-004.md) |
| **BV-11** | `email="a@b.co"` (TLD ngắn hợp lệ) | 200 OK | Đăng ký thành công | Chấp nhận đăng ký | **PASS** | — |
| **BV-12** | `email="a@b.c"` (TLD không hợp lệ) | 200 OK | Đăng ký thành công | Từ chối đăng ký | **FAIL** | [BUG-002](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-002.md) |

---

## 3. Nhật ký thực thi UI / Code Review (Frontend Web)

Phát hiện lỗi bằng cách duyệt ứng dụng thực tế trên trình duyệt và đối chiếu mã nguồn của `Register.jsx`:

| TC-ID | Nội dung kiểm thử | Kết quả thực tế (Code & UI) | Kết quả mong đợi (SRS) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-------------------|-----------------------------|------------------------|---------------------|-----------------|
| **DT-10** | Xác nhận mật khẩu không khớp | **Không kiểm tra được** vì form không có trường Confirm Password | Phải báo lỗi và chặn submit | **FAIL** | [BUG-005](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-005.md) |
| **DT-11** | Có trường Xác nhận mật khẩu trên UI | **Không có** trường "Xác nhận mật khẩu" trên giao diện | Phải hiển thị trường nhập Xác nhận mật khẩu | **FAIL** | [BUG-005](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/BUG-005.md) |
| **DT-07** | Nhập pass hợp lệ SRS `"Test1234!"` | Bị client chặn và hiển thị thông báo mật khẩu quá yếu | Chấp nhận và submit thành công | **FAIL** | [BUG-006](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-006.md) |
| **DT-08** | Nhập pass có khoảng trắng `"Test 1234"` | Client **chấp nhận** và cho phép submit đăng ký | Phải từ chối vì thiếu ký tự đặc biệt | **FAIL** | [BUG-006](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-006.md) |
| **DT-01 (UI)** | Đăng ký thành công điều hướng về Login | Sau khi submit thành công, gọi `navigate('/login')` chuyển trang | Phải chuyển hướng về `/login` | **PASS** | — |
| **DT-04 (UI)** | Email type attribute | Trường nhập Email có thuộc tính `type="text"` | Phải có thuộc tính `type="email"` | **FAIL** | [BUG-007](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs/BUG-007.md) |

---

## 4. Đánh giá & Khuyến nghị

- **Phía Backend:** Hoàn toàn bỏ ngỏ khâu validate (Zero validation). Cần lập tức thêm thư viện validate (như `joi` hoặc `express-validator`) để kiểm tra dữ liệu đầu vào tại endpoint `POST /api/register` và thêm ràng buộc `UNIQUE` vào cột `email` của bảng `users`.
- **Phía Frontend:** Cần viết lại Regex mật khẩu mạnh để khớp đúng đặc tả SRS (yêu cầu ký tự đặc biệt `@$!%*?&` và loại bỏ ép buộc khoảng trắng `\s`). Đồng thời bổ sung ô nhập "Xác nhận mật khẩu" (`confirmPassword`) và logic kiểm tra khớp mật khẩu trước khi gửi request.
- **An toàn thông tin:** Hiện tại mật khẩu đang lưu dạng plaintext (chưa hash). Cần sử dụng thư viện mã hóa mật khẩu như `bcryptjs` trước khi lưu vào DB.
