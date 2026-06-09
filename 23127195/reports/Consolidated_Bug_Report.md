# Consolidated Bug Report — EShop Testing

**MSSV:** 23127195  
**SUT:** Giao diện Checkout, Register + API Backend + Database

---

# FEATURE: FR-01 — ĐĂNG KÝ TÀI KHOẢN (8 BUGS)

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
- ![BUG-001](./FR-01_bugs/BUG-001.png)

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
- ![BUG-002](./FR-01_bugs/BUG-002.png)

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
- ![BUG-003](./FR-01_bugs/BUG-003.png)

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
- ![BUG-004](./FR-01_bugs/BUG-004.png)

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
- ![BUG-005](./FR-01_bugs/BUG-005.png)

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
- ![BUG-006](./FR-01_bugs/BUG-006.png)

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
- ![BUG-007](./FR-01_bugs/BUG-007.png)

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
- ![BUG-008](./FR-01_bugs/BUG-008.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-01] [BUG-008] Mật khẩu người dùng được lưu trữ dưới dạng Plaintext trong Database`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/10

---
---

# FEATURE: FR-09 — MÃ GIẢM GIÁ (5 BUGS)

### BUG-001: API apply-coupon chặn sai logic biên dưới đơn hàng tối thiểu

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API
- **Test Case liên quan:** BV-02, BV-05
- **Liên quan SRS:** Đơn hàng phải lớn hơn hoặc bằng (`>=`) giá trị `min_order_amount`.

#### Lệnh chạy test thực tế (PowerShell):
```powershell
# Mã SAVE10 có min_order_amount = 300,000 ₫. Gửi đơn hàng trị giá đúng 300,000 ₫
Invoke-RestMethod -Uri "http://localhost:3000/api/apply-coupon" -Method Post -ContentType "application/json" -Body '{"code":"SAVE10","total_amount":300000,"user_id":2}'
```

#### Kết quả mong đợi (Expected Result):
- Chấp nhận áp dụng mã thành công, giảm 10% (30,000 ₫), trả về HTTP 200 OK.

#### Kết quả thực tế (Actual Result):
- Trả về HTTP 400 Bad Request: `{"error":"Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này"}`. Do backend check `total_amount > coupon.min_order_amount` (lớn hơn hẳn) thay vì `>=`.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-001](./FR-09_bugs/BUG-001.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-09] [BUG-001] API apply-coupon chặn sai logic biên dưới đơn hàng tối thiểu`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/11

---

### BUG-002: Sai lệch nghiêm trọng công thức tính toán giảm giá theo phần trăm (percent)

- **Độ nghiêm trọng (Severity):** Critical
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API
- **Test Case liên quan:** DT-01, EP-TYP1
- **Liên quan SRS:** Loại `percent`: `discount_amount = total × discount_value / 100`.

#### Lệnh chạy test thực tế (PowerShell):
```powershell
# Gửi đơn hàng trị giá 350,000 ₫ với mã SAVE10 (giảm 10%)
Invoke-RestMethod -Uri "http://localhost:3000/api/apply-coupon" -Method Post -ContentType "application/json" -Body '{"code":"SAVE10","total_amount":350000,"user_id":2}'
```

#### Kết quả mong đợi (Expected Result):
- Tiết kiệm: `35,000 ₫` (10% của 350k).
- Thành tiền: `315,000 ₫` (350k - 35k).

#### Kết quả thực tế (Actual Result):
- Trả về HTTP 200 OK nhưng tính sai tiền: `discount_amount: -3150000` và `final_amount: 3500000` (lỗi nhân checkout cost lên 10 lần và giảm âm). Do dòng 400 của `server.js` dùng công thức: `total_amount * (1 - coupon.discount_value)` với `discount_value = 10`, tạo ra `-9 * total_amount`.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-002](./FR-09_bugs/BUG-002.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-09] [BUG-002] Sai lệch nghiêm trọng công thức tính toán giảm giá theo phần trăm`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/12

---

### BUG-003: API apply-coupon thiếu middleware xác thực JWT (Authentication Bypass)

- **Độ nghiêm trọng (Severity):** Critical
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API / Security
- **Test Case liên quan:** DT-07, EP-AUTH2
- **Liên quan SRS:** Người dùng phải đăng nhập hệ thống (có JWT token hợp lệ gửi kèm) để được áp dụng mã.

#### Lệnh chạy test thực tế (PowerShell):
```powershell
# Gửi request áp dụng mã mà hoàn toàn không đính kèm Header Authorization (token JWT)
Invoke-RestMethod -Uri "http://localhost:3000/api/apply-coupon" -Method Post -ContentType "application/json" -Body '{"code":"SAVE10","total_amount":350000}'
```

#### Kết quả mong đợi (Expected Result):
- Từ chối áp dụng mã, trả về HTTP 401 Unauthorized / HTTP 403 Forbidden.

#### Kết quả thực tế (Actual Result):
- API trả về HTTP 200 OK và áp dụng mã thành công cho khách vãng lai (Guest).

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-003](./FR-09_bugs/BUG-003.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-09] [BUG-003] API apply-coupon thiếu middleware xác thực JWT`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/13

---

### BUG-004: API cho phép giả mạo ID người dùng trong body để vượt giới hạn lượt dùng

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API / Security
- **Test Case liên quan:** DT-10, C-04
- **Liên quan SRS:** Ràng buộc bảo mật (Không cho phép gửi user_id giả mạo để bypass giới hạn lượt dùng tối đa của user hiện tại).

#### Lệnh chạy test thực tế (PowerShell):
```powershell
# Tài khoản đang đăng nhập có user_id = 2 (đã dùng mã SAVE10). 
# Gửi request đính kèm token của user 2, nhưng trong body gửi user_id = 999 (ID chưa từng dùng mã)
Invoke-RestMethod -Uri "http://localhost:3000/api/apply-coupon" -Headers @{ Authorization = "Bearer <Token_User_2>" } -Method Post -ContentType "application/json" -Body '{"code":"SAVE10","total_amount":350000,"user_id":999}'
```

#### Kết quả mong đợi (Expected Result):
- Hệ thống phải tự lấy `user.id` từ JWT token để đếm lượt dùng, hoặc từ chối do `user_id` trong body không khớp với token.

#### Kết quả thực tế (Actual Result):
- API chấp nhận áp dụng mã giảm giá thành công cho user 999, vượt qua kiểm tra `max_uses_per_user` của user 2.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-004](./FR-09_bugs/BUG-004.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-09] [BUG-004] API cho phép giả mạo ID người dùng để vượt giới hạn sử dụng`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/14

---

### BUG-005: Cho phép người dùng chỉnh sửa giá trị tổng thanh toán và Checkout thành công với giá tùy ý

- **Độ nghiêm trọng (Severity):** Critical
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** Web UI / API
- **Test Case liên quan:** FR-08 / Code Review
- **Liên quan SRS:** Ràng buộc nghiệp vụ thanh toán (Giá trị thanh toán phải được tính toán tự động dựa trên giỏ hàng và mã giảm giá, không được cho người dùng tự ý chỉnh sửa).

#### Các bước tái hiện / Khảo sát mã nguồn:
1. Truy cập màn hình Checkout tại `http://localhost:5173/checkout`.
2. Trường "Tổng tiền thanh toán (VND)" hiển thị dưới dạng một ô nhập số (`<input type="number">`), cho phép người dùng nhập tự do bất cứ số tiền nào (ví dụ sửa thành `1` ₫).
3. Bấm "Thanh toán". Backend API `/api/checkout` chấp nhận lưu số tiền này trực tiếp vào bảng `orders` mà không thực hiện kiểm tra chéo giá trị thực tế của sản phẩm.

#### Kết quả mong đợi (Expected Result):
- Giao diện không cho phép chỉnh sửa ô "Tổng tiền thanh toán".
- API checkout phải tự tính lại tổng tiền từ DB sản phẩm và từ chối nếu số tiền gửi lên sai lệch.

#### Kết quả thực tế (Actual Result):
- Người dùng có thể chỉnh sửa tổng tiền tùy ý trên UI, và backend checkout thành công với bất kỳ số tiền nào (kể cả 1 ₫).

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-005](./FR-09_bugs/BUG-005.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-09] [BUG-005] Cho phép chỉnh sửa tổng tiền thanh toán và Checkout với giá tùy ý`
- **Link Issue:** https://github.com/hungtmh/HW02-Domain_Testing/issues/15
