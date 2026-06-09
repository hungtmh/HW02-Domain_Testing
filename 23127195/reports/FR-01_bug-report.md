# Consolidated Bug Report — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**SUT:** Frontend Web (`http://localhost:5173`) + Backend API (`http://localhost:3000`)

---

## Danh sách tổng hợp lỗi phát hiện (API Validation Bypass & UI Defects)

### BUG-001: API cho phép đăng ký trùng email

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API / Database
- **Test Case liên quan:** DT-02, BV-12
- **Liên quan SRS:** Email phải có định dạng hợp lệ (`user@domain.com`) và là **duy nhất** trong hệ thống.

#### Lệnh chạy test thực tế:
```powershell
# Chạy khi backend đang khởi chạy (đăng ký lại email test@eshop.com đã được seed sẵn)
Invoke-RestMethod -Uri "http://localhost:3000/api/register" -Method Post -ContentType "application/json" -Body '{"name":"Nguyen Van A","email":"test@eshop.com","password":"Test1234!"}'
```

#### Kết quả mong đợi (Expected Result):
- API trả về lỗi xác thực (HTTP 400 hoặc 409) thông báo email đã tồn tại.

#### Kết quả thực tế (Actual Result):
- Trả về HTTP 200 OK: `{"message":"User registered successfully","id":10}`.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn screenshot tại đây: `![BUG-001](./FR-01_bugs/BUG-001.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-001] API cho phép đăng ký trùng email`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/3

---

### BUG-002: API cho phép đăng ký email sai định dạng

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API
- **Test Case liên quan:** DT-03, BV-12
- **Liên quan SRS:** Email phải có định dạng hợp lệ (`user@domain.com`).

#### Lệnh chạy test thực tế:
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/register" -Method Post -ContentType "application/json" -Body '{"name":"Nguyen Van A","email":"invalid-email","password":"Test1234!"}'
```

#### Kết quả mong đợi (Expected Result):
- API từ chối đăng ký và trả về HTTP 400 Bad Request.

#### Kết quả thực tế (Actual Result):
- Trả về HTTP 200 OK: `{"message":"User registered successfully","id":11}`.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn screenshot tại đây: `![BUG-002](./FR-01_bugs/BUG-002.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-002] API cho phép đăng ký email sai định dạng`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/4

---

### BUG-003: API cho phép đăng ký khi bỏ trống các trường bắt buộc

- **Độ nghiêm trọng (Severity):** Critical
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API / Database
- **Test Case liên quan:** DT-04, DT-05, BV-10
- **Liên quan SRS:** Người dùng phải cung cấp: **Họ Tên**, **Email**, **Mật khẩu**.

#### Lệnh chạy test thực tế:
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/register" -Method Post -ContentType "application/json" -Body '{}'
```

#### Kết quả mong đợi (Expected Result):
- API từ chối đăng ký và trả về HTTP 400 Bad Request.

#### Kết quả thực tế (Actual Result):
- Trả về HTTP 200 OK: `{"message":"User registered successfully","id":12}` (Lưu các cột `name`, `email`, `password` đều có giá trị `NULL` vào DB).

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn screenshot tại đây: `![BUG-003](./FR-01_bugs/BUG-003.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-003] API cho phép đăng ký tài khoản rỗng (NULL)`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/5

---

### BUG-004: API không xác thực độ mạnh mật khẩu

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API
- **Test Case liên quan:** BV-01, BV-04, BV-07, BV-08
- **Liên quan SRS:** **Yêu cầu mật khẩu mạnh**: Tối thiểu 8 ký tự, có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số và 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`).

#### Lệnh chạy test thực tế:
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/register" -Method Post -ContentType "application/json" -Body '{"name":"Nguyen Van A","email":"weak_pw@test.com","password":"123"}'
```

#### Kết quả mong đợi (Expected Result):
- API từ chối đăng ký do mật khẩu quá ngắn và yếu (HTTP 400 Bad Request).

#### Kết quả thực tế (Actual Result):
- Trả về HTTP 200 OK và lưu mật khẩu `"123"` vào DB.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn screenshot tại đây: `![BUG-004](./FR-01_bugs/BUG-004.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-004] API Backend không xác thực độ mạnh mật khẩu`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/6

---

### BUG-005: Thiếu trường Xác nhận mật khẩu trên UI Frontend

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** Web UI
- **Test Case liên quan:** DT-10, DT-11
- **Liên quan SRS:** Phải có trường **Xác nhận mật khẩu** — hệ thống từ chối nếu hai trường không khớp.

#### Các bước tái hiện:
1. Mở trình duyệt và truy cập trang đăng ký `http://localhost:5173/register`.
2. Kiểm tra trực quan danh sách các trường nhập liệu trên form.

#### Kết quả mong đợi (Expected Result):
- Có trường "Xác nhận mật khẩu" (Confirm Password) để nhập dữ liệu đối chiếu.

#### Kết quả thực tế (Actual Result):
- Chỉ hiển thị 3 trường: Họ Tên, Email, Mật khẩu. Hoàn toàn không có trường Xác nhận mật khẩu.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn screenshot giao diện đăng ký thiếu trường tại đây: `![BUG-005](./FR-01_bugs/BUG-005.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-005] Thiếu trường Xác nhận mật khẩu trên form đăng ký`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/7

---

### BUG-006: Regex kiểm tra mật khẩu mạnh ở Frontend bị sai (yêu cầu khoảng trắng)

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** Web UI
- **Test Case liên quan:** DT-07, DT-08, BV-08
- **Liên quan SRS:** Mật khẩu mạnh: Tối thiểu 8 ký tự, có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số và 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`).

#### Các bước tái hiện:
1. Mở trang đăng ký tài khoản `http://localhost:5173/register`.
2. Nhập Họ Tên và Email hợp lệ.
3. Ở ô Mật khẩu, nhập mật khẩu hợp lệ SRS: `"Test1234!"` -> Click "Đăng ký" -> Bị chặn và báo mật khẩu yếu.
4. Ở ô Mật khẩu, nhập mật khẩu có khoảng trắng, không ký tự đặc biệt: `"Test 1234"` -> Click "Đăng ký" -> Form chấp nhận gửi lên API.

#### Kết quả mong đợi (Expected Result):
- `"Test1234!"` được chấp nhận.
- `"Test 1234"` bị từ chối do thiếu ký tự đặc biệt.

#### Kết quả thực tế (Actual Result):
- `"Test1234!"` bị chặn vì không có khoảng trắng.
- `"Test 1234"` được thông qua vì regex của client (`flawedStrongPasswordRegex` tại `Register.jsx` dòng 15) yêu cầu khoảng trắng `\s` thay vì ký tự đặc biệt.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn screenshot tại đây: `![BUG-006](./FR-01_bugs/BUG-006.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-006] Regex validate mật khẩu ở Frontend yêu cầu khoảng trắng thay vì ký tự đặc biệt`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/8

---

### BUG-007: Màn hình Đăng ký sử dụng ô nhập email kiểu type="text"

- **Độ nghiêm trọng (Severity):** Minor
- **Độ ưu tiên (Priority):** Low
- **Thành phần ảnh hưởng (Component):** Web UI
- **Test Case liên quan:** DT-04 (UI)
- **Liên quan SRS:** Chuẩn thiết kế UI tối ưu cho người dùng.

#### Các bước tái hiện:
1. Mở `http://localhost:5173/register`.
2. Inspect phần tử ô nhập Email để xem thuộc tính HTML.

#### Kết quả mong đợi (Expected Result):
- Thuộc tính thẻ input có: `<input type="email" ... />`.

#### Kết quả thực tế (Actual Result):
- Thuộc tính thẻ input là: `<input type="text" ... />` (Dòng 48 file `Register.jsx`).

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn screenshot Inspect HTML tại đây: `![BUG-007](./FR-01_bugs/BUG-007.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-007] Màn hình Đăng ký sử dụng ô nhập email kiểu type="text"`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/9

---

### BUG-008: Mật khẩu người dùng được lưu trữ dưới dạng Plaintext trong Database

- **Độ nghiêm trọng (Severity):** Critical
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API / Database
- **Test Case liên quan:** DT-01 / Code Review
- **Liên quan SRS:** Ràng buộc an toàn thông tin cơ bản (Mật khẩu phải được mã hóa trước khi lưu trữ).

#### Các bước tái hiện:
1. Đăng ký tài khoản thành công.
2. Kiểm tra trực tiếp bảng `users` trong cơ sở dữ liệu `database.sqlite` hoặc file seed dữ liệu [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js) dòng 91-94.

#### Kết quả mong đợi (Expected Result):
- Mật khẩu phải được hash/băm trước khi lưu (ví dụ: `$2a$10$...`).

#### Kết quả thực tế (Actual Result):
- Mật khẩu mẫu và mật khẩu người dùng mới đều được lưu trữ trực tiếp bằng Plaintext (ví dụ: `"Admin123!"`).

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- *[Chèn ảnh chụp màn hình dữ liệu database bị lộ mật khẩu plaintext tại đây: `![BUG-008](./FR-01_bugs/BUG-008.png)`]*

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-008] Mật khẩu người dùng được lưu trữ dưới dạng Plaintext trong Database`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/10
