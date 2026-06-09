# Consolidated Bug Report — FR-09: Mã Giảm Giá & Thanh Toán

**MSSV:** 23127195  
**SUT:** Giao diện Checkout (`http://localhost:5173/checkout`) + Backend API (`http://localhost:3000`)

---

## Danh sách tổng hợp lỗi phát hiện (Defects List)

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
