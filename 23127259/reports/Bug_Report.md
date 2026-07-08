# Consolidated Bug Report - EShop Testing

**Họ và tên:** Nguyễn Tấn Thắng  
**Nhóm:** Nhóm 08  
**MSSV:** 23127259  
**Ngày cập nhật:** 2026-07-06  
**SUT:** Web Client + Web Admin + Mobile App + API Backend

**Evidence run:** 2026-07-05 20:13 ICT, test data prefix `live_hw02_1783257224503`. Ảnh/video bug trong các thư mục evidence là minh chứng từ thao tác UI/API trực tiếp trên EShop SUT. Riêng FR-07 BUG-003 dùng video `.mov`; PDF dùng ảnh preview để hiển thị ổn định.

---

# Bug Report - FR-02 Login and Account Lockout

## BUG-FR02-001: Failed login counter increases by 2 instead of 1

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** API Backend
- **Test Case liên quan:** DT-03, DT-04, DT-05 / BV-01, BV-02, BV-03
- **Liên quan SRS:** "Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên đúng 1 đơn vị." (FR-02)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Sử dụng tài khoản test có sẵn `test@eshop.com`.
2. Truy cập CSDL SQLite để xác nhận `login_attempts = 0` bằng cách chạy query:
```sql
SELECT login_attempts FROM users WHERE email = 'test@eshop.com';
```
3. Thực hiện gửi 1 request đăng nhập sai password thông qua PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/login" -Method Post -ContentType "application/json" -Body '{"email": "test@eshop.com", "password": "WrongPassword123"}'
```
Hoặc bằng `curl` trong macOS/Linux:
```bash
curl -X POST http://localhost:3000/api/login -H "Content-Type: application/json" -d '{"email": "test@eshop.com", "password": "WrongPassword123"}'
```
4. Kiểm tra lại giá trị cột `login_attempts` trong CSDL SQLite:
```sql
SELECT login_attempts FROM users WHERE email = 'test@eshop.com';
```

#### Kết quả mong đợi (Expected Result):
- Sau 1 lần đăng nhập sai, `login_attempts` được cập nhật thành `1`.

#### Kết quả thực tế (Actual Result):
- Sau 1 lần đăng nhập sai, `login_attempts` tăng lên thành `2` (và tăng lên `4` ở lần 2, dẫn đến việc bị khóa tài khoản ngay lập tức khi chưa đủ 3 lần đăng nhập sai).
- Đoạn code gây lỗi tại [server.js:L54](../../backend/server.js#L54):
```javascript
const newAttempts = user.login_attempts + 2;
```

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-FR02-001](./FR-02_bugs/BUG-001.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-02] [BUG-001] Failed login counter increases by 2 instead of 1`
- **Link Issue:** [#27](https://github.com/hungtmh/HW02-Domain_Testing/issues/27)

---

## BUG-FR02-002: Account lockout duration is 180 seconds instead of 30 seconds

- **Độ nghiêm trọng (Severity):** Medium
- **Độ ưu tiên (Priority):** Medium
- **Thành phần ảnh hưởng (Component):** API Backend
- **Test Case liên quan:** DT-06 / BV-04, BV-05, BV-06
- **Liên quan SRS:** "Nếu đăng nhập sai từ 3 lần trở lên liên tiếp, tài khoản bị tạm khóa 30 giây (môi trường demo)." (FR-02)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Kích hoạt khóa tài khoản bằng cách đăng nhập sai liên tiếp để `login_attempts >= 3` (gọi API login sai 2 lần do lỗi counter tăng 2).
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/login" -Method Post -ContentType "application/json" -Body '{"email": "test@eshop.com", "password": "WrongPassword123"}'
```
2. Kiểm tra giá trị cột `locked_until` trong CSDL SQLite:
```sql
SELECT locked_until FROM users WHERE email = 'test@eshop.com';
```
3. Tính toán khoảng chênh lệch giữa giá trị cột `locked_until` và thời điểm thực hiện request.

#### Kết quả mong đợi (Expected Result):
- Tài khoản bị khóa trong vòng 30 giây (giá trị `locked_until` bằng thời gian gửi request cộng thêm 30000ms).

#### Kết quả thực tế (Actual Result):
- Tài khoản bị khóa trong vòng 180 giây (3 phút) do server.js thiết lập cộng thêm 180000ms.
- Đoạn code gây lỗi tại [server.js:L57](../../backend/server.js#L57):
```javascript
lockedUntil = new Date(Date.now() + 180000).toISOString();
```

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-FR02-002](./FR-02_bugs/BUG-002.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-02] [BUG-002] Account lockout duration is 180 seconds instead of 30 seconds`
- **Link Issue:** [#28](https://github.com/hungtmh/HW02-Domain_Testing/issues/28)

---

## BUG-FR02-003: Login page violates multiple HTML5 & GUI guidelines (Form fields, label, tabOrder, and error position)

- **Độ nghiêm trọng (Severity):** Minor
- **Độ ưu tiên (Priority):** Medium
- **Thành phần ảnh hưởng (Component):** Frontend Web Login
- **Test Case liên quan:** DT-07 / BV-06
- **Liên quan SRS:** 
  - "Trường email phải dùng type=\"email\" (có validate HTML5 format)." (FR-02 / FR-22)
  - "Trường Mật khẩu phải dùng type=\"password\" (không hiển thị rõ)." (FR-22)
  - "Thông báo lỗi phải xuất hiện trên nút submit, không phải bên dưới." (FR-22)
  - "Thứ tự focus theo Tab phải đi từ trên xuống dưới, trái sang phải." (FR-21)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Mở trình duyệt và truy cập trang đăng nhập tại địa chỉ `http://localhost:5173/login`.
2. Kiểm tra tiêu đề form đăng nhập, các nhãn (labels) và kiểu (type) của ô nhập liệu (input).
3. Kiểm tra vị trí hiển thị của thông báo lỗi khi đăng nhập thất bại.
4. Bấm phím Tab để kiểm tra thứ tự chuyển focus.

#### Kết quả mong đợi (Expected Result):
- Tiêu đề form là "Đăng Nhập". Nhãn ô Email là "Email" với input `type="email"`.
- Ô Mật khẩu có input `type="password"`.
- Thứ tự Tab di chuyển tuần tự: Email -> Mật khẩu -> Quên mật khẩu -> Nút Sign In.
- Thông báo lỗi hiển thị nằm ở phía trên nút submit.

#### Kết quả thực tế (Actual Result):
- Tiêu đề form bị hiển thị sai thành "Đăng Ký".
- Nhãn của ô nhập email hiển thị là "Username" và thẻ input sử dụng `type="text"`.
- Ô nhập mật khẩu sử dụng `type="text"`, khiến mật khẩu hiển thị dưới dạng văn bản thường khi nhập.
- Nút submit có thuộc tính `tabIndex={1}`, phá hỏng luồng focus bàn phím tự nhiên.
- Khối hiển thị lỗi `{error && ...}` đặt ở dòng cuối cùng của component, nằm bên dưới nút submit.
- Đoạn code gây lỗi tại [Login.jsx](../../frontend-web/src/pages/Login.jsx):
  - [L24](../../frontend-web/src/pages/Login.jsx#L24): `<h2 className="...">Đăng Ký</h2>`
  - [L28](../../frontend-web/src/pages/Login.jsx#L28): `<label className="...">Username</label>`
  - [L30](../../frontend-web/src/pages/Login.jsx#L30): `<input type="text" ... />` (cho email)
  - [L40](../../frontend-web/src/pages/Login.jsx#L40): `<input type="text" ... />` (cho password)
  - [L56](../../frontend-web/src/pages/Login.jsx#L56): `tabIndex={1}` trên nút submit
  - [L66](../../frontend-web/src/pages/Login.jsx#L66): Thẻ hiển thị lỗi `{error && <div className="...">...</div>}` nằm dưới nút submit.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-FR02-003](./FR-02_bugs/BUG-003.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-02] [BUG-003] Login page violates HTML5 & GUI guidelines`
- **Link Issue:** [#29](https://github.com/hungtmh/HW02-Domain_Testing/issues/29)

---

# Bug Report - FR-07 Shopping Cart

## BUG-FR07-001: Adding same product creates duplicate rows

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** Frontend Web / API Backend
- **Test Case liên quan:** FR07-TC03 / DT-03
- **Liên quan SRS:** "Thêm cùng một sản phẩm vào giỏ sẽ tăng số lượng, không tạo dòng mới." (FR-07)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Đăng nhập bằng tài khoản test (lấy token).
2. Gọi API thêm sản phẩm A (ví dụ ID: 1) vào giỏ hàng:
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/cart" -Method Post -Headers @{ Authorization = "Bearer <token>" } -ContentType "application/json" -Body '{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": 1}'
```
3. Tiếp tục gọi API thêm sản phẩm A lần thứ 2 với số lượng là 1:
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/cart" -Method Post -Headers @{ Authorization = "Bearer <token>" } -ContentType "application/json" -Body '{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": 1}'
```
4. Lấy danh sách sản phẩm trong giỏ hàng:
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/cart" -Method Get -Headers @{ Authorization = "Bearer <token>" }
```

#### Kết quả mong đợi (Expected Result):
- Giỏ hàng trả về 1 dòng duy nhất cho sản phẩm A với số lượng (`quantity`) bằng 2.

#### Kết quả thực tế (Actual Result):
- Giỏ hàng trả về 2 dòng riêng biệt cho sản phẩm A, mỗi dòng có số lượng bằng 1.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-FR07-001](./FR-07_bugs/BUG-001.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-07] [BUG-001] Adding same product creates duplicate rows`
- **Link Issue:** [#30](https://github.com/hungtmh/HW02-Domain_Testing/issues/30)

---

## BUG-FR07-002: Cart quantity has no `+/-` controls

- **Độ nghiêm trọng (Severity):** Major
- **Độ ưu tiên (Priority):** High
- **Thành phần ảnh hưởng (Component):** Frontend Web
- **Test Case liên quan:** FR07-TC04
- **Liên quan SRS:** "Hiển thị danh sách sản phẩm với các cột: Sản phẩm, Đơn giá, Số lượng (có nút +/- để chỉnh), Thành tiền, Thao tác." (FR-07)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Thêm một sản phẩm bất kỳ vào giỏ hàng.
2. Truy cập trang giỏ hàng tại địa chỉ `http://localhost:5173/cart`.
3. Kiểm tra cột "Số lượng" trên giao diện giỏ hàng.

#### Kết quả mong đợi (Expected Result):
- Có các nút tăng/giảm (`+` và `-`) bên cạnh con số hiển thị số lượng để người dùng chỉnh sửa.

#### Kết quả thực tế (Actual Result):
- Cột số lượng chỉ hiển thị số lượng dưới dạng văn bản tĩnh (ví dụ: `1`), không có bất kỳ nút tăng/giảm hay ô nhập liệu nào.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-FR07-002](./FR-07_bugs/BUG-002.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-07] [BUG-002] Cart quantity has no +/- controls`
- **Link Issue:** [#31](https://github.com/hungtmh/HW02-Domain_Testing/issues/31)

---

## BUG-FR07-003: Delete cart item does not show confirmation dialog

- **Độ nghiêm trọng (Severity):** Medium
- **Độ ưu tiên (Priority):** Medium
- **Thành phần ảnh hưởng (Component):** Frontend Web
- **Test Case liên quan:** FR07-TC05
- **Liên quan SRS:** "Nút Xóa sản phẩm phải có dialog xác nhận trước khi thực hiện." (FR-07)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Thêm một sản phẩm vào giỏ hàng.
2. Truy cập trang giỏ hàng `http://localhost:5173/cart`.
3. Nhấp vào nút "Xóa" tại cột "Thao tác" của sản phẩm đó.

#### Kết quả mong đợi (Expected Result):
- Hệ thống hiển thị hộp thoại xác nhận (dialog) hỏi người dùng xem họ có chắc chắn muốn xóa sản phẩm đó hay không.

#### Kết quả thực tế (Actual Result):
- Sản phẩm bị xóa ngay lập tức khỏi giỏ hàng mà không có bất kỳ hộp thoại xác nhận nào được hiển thị.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- [Open video evidence: BUG-003.mov](./FR-07_bugs/BUG-003.mov)
- ![BUG-FR07-003 preview](./FR-07_bugs/BUG-003-preview.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-07] [BUG-003] Delete cart item does not show confirmation dialog`
- **Link Issue:** [#32](https://github.com/hungtmh/HW02-Domain_Testing/issues/32)

---

## BUG-FR07-004: Cart total label is wrong

- **Độ nghiêm trọng (Severity):** Medium
- **Độ ưu tiên (Priority):** Medium
- **Thành phần ảnh hưởng (Component):** Frontend Web
- **Test Case liên quan:** FR07-TC07
- **Liên quan SRS:** "Tổng tiền hiển thị nhãn chính xác: 'Tổng cộng' (không phải 'Tổng tạm tính')." (FR-07)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Thêm sản phẩm vào giỏ hàng.
2. Truy cập trang giỏ hàng `http://localhost:5173/cart`.
3. Quan sát nhãn tiêu đề của dòng tổng tiền nằm ở dưới góc trái/phải bảng.

#### Kết quả mong đợi (Expected Result):
- Nhãn hiển thị là `"Tổng cộng"`.

#### Kết quả thực tế (Actual Result):
- Nhãn hiển thị trên giao diện là `"Tổng tạm tính:"`.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-FR07-004](./FR-07_bugs/BUG-004.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-07] [BUG-004] Cart total label is wrong`
- **Link Issue:** [#33](https://github.com/hungtmh/HW02-Domain_Testing/issues/33)

---

## BUG-FR07-005: Empty cart has no illustration

- **Độ nghiêm trọng (Severity):** Minor
- **Độ ưu tiên (Priority):** Low
- **Thành phần ảnh hưởng (Component):** Frontend Web
- **Test Case liên quan:** FR07-TC01
- **Liên quan SRS:** "Giỏ hàng trống phải có hình minh họa và thông báo rõ ràng." (FR-07)

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. Mở trang giỏ hàng `http://localhost:5173/cart` khi chưa có sản phẩm nào.

#### Kết quả mong đợi (Expected Result):
- Giao diện hiển thị hình ảnh minh họa sinh động/icon giỏ hàng trống cùng với thông báo rõ ràng.

#### Kết quả thực tế (Actual Result):
- Giao diện chỉ có dòng chữ `"Giỏ hàng của bạn đang trống"` và đường dẫn `"Tiếp tục mua sắm"`, không có hình ảnh/hình vẽ minh họa nào kèm theo.

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- ![BUG-FR07-005](./FR-07_bugs/BUG-005.png)

#### Thông tin GitHub Issue:
- **Title:** `[FR-07] [BUG-005] Empty cart has no illustration`
- **Link Issue:** [#34](https://github.com/hungtmh/HW02-Domain_Testing/issues/34)

---

# Bug Report - FR-16 Product Import from CSV

## BUG-FR16-001: Normal user can call admin product import API

- **GitHub Issue:** [#35](https://github.com/hungtmh/HW02-Domain_Testing/issues/35)

- **Severity:** Critical
- **Priority:** High
- **Component:** API Backend / Access Control
- **Related test cases:** FR16-TC04

**Expected:** Normal user token is rejected with HTTP 403 and no product is inserted.

**Actual:** Normal user token receives HTTP 200 and the product is inserted.

**Evidence:**

![BUG-FR16-001](./FR-16_bugs/BUG-001.png)

---

## BUG-FR16-002: Product import is not atomic when a row is invalid

- **GitHub Issue:** [#36](https://github.com/hungtmh/HW02-Domain_Testing/issues/36)

- **Severity:** Major
- **Priority:** High
- **Component:** API Backend / Database
- **Related test cases:** FR16-TC05

**Expected:** If any row is invalid, the whole import is rejected and rolled back.

**Actual:** API reports `inserted = 1/2`; the valid row is still inserted even though another row has an error.

**Evidence:**

![BUG-FR16-002 step 1](./FR-16_bugs/BUG-002-1.png)

![BUG-FR16-002 step 2](./FR-16_bugs/BUG-002-2.png)

---

## BUG-FR16-003: Product import accepts negative price

- **GitHub Issue:** [#37](https://github.com/hungtmh/HW02-Domain_Testing/issues/37)

- **Severity:** Major
- **Priority:** High
- **Component:** API Backend Validation
- **Related test cases:** FR16-TC06

**Expected:** Product with `price <= 0` is rejected.

**Actual:** Product with negative price is inserted.

**Evidence:**

![BUG-FR16-003](./FR-16_bugs/BUG-003.png)

---

## BUG-FR16-004: CSV parser does not support quoted commas

- **GitHub Issue:** [#38](https://github.com/hungtmh/HW02-Domain_Testing/issues/38)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Web Admin CSV Import
- **Related test cases:** FR16-TC07

**Expected:** CSV fields wrapped in double quotes can contain commas.

**Actual:** Admin parser uses `line.split(",")`, so quoted commas break the column mapping.

**Evidence:**

![BUG-FR16-004](./FR-16_bugs/BUG-004.png)

---

# Bug Report - Mobile Product Listing/Search

## BUG-MOB-001: Mobile API URL is hard-coded

- **GitHub Issue:** [#39](https://github.com/hungtmh/HW02-Domain_Testing/issues/39)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Mobile App Config
- **Related test cases:** MOB-TC05

**Expected:** API URL is configurable by environment/device.

**Actual:** `API_URL` is hard-coded to a LAN IP, making product listing/search fail on other devices or emulators.

**Evidence:**

![BUG-MOB-001](./Mobile-product-listing_bugs/BUG-001.jpg)

---

## BUG-MOB-002: Search query is not URL-encoded

- **GitHub Issue:** [#40](https://github.com/hungtmh/HW02-Domain_Testing/issues/40)

- **Severity:** Major
- **Priority:** High
- **Component:** Mobile Product Search
- **Related test cases:** MOB-TC04

**Expected:** Search keyword with special characters is URL-encoded.

**Actual:** Search query is concatenated directly into the URL.

**Evidence:**

![BUG-MOB-002](./Mobile-product-listing_bugs/BUG-002.jpg)

---

## BUG-MOB-003: Product search has no empty state

- **GitHub Issue:** [#41](https://github.com/hungtmh/HW02-Domain_Testing/issues/41)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Mobile Product Listing
- **Related test cases:** MOB-TC03

**Expected:** No-result search shows a clear empty state message.

**Actual:** Empty result does not show a proper empty state.

**Evidence:**

![BUG-MOB-003](./Mobile-product-listing_bugs/BUG-003.jpg)

---

## BUG-MOB-004: Product images use `resizeMode="stretch"`

- **GitHub Issue:** [#42](https://github.com/hungtmh/HW02-Domain_Testing/issues/42)

- **Severity:** Minor
- **Priority:** Low
- **Component:** Mobile Product Listing / Detail
- **Related test cases:** MOB-TC07

**Expected:** Product images preserve their aspect ratio.

**Actual:** Product images are stretched and can appear distorted.

**Evidence:**

![BUG-MOB-004](./Mobile-product-listing_bugs/BUG-004.jpg)

---

## GitHub Issues

Các bug đã được tạo issue thật trên GitHub repo nhóm để team có thể theo dõi và xử lý:

- **BUG-FR02-001:** [#27](https://github.com/hungtmh/HW02-Domain_Testing/issues/27) - [FR-02] [BUG-001] Failed login counter increases by 2 instead of 1
- **BUG-FR02-002:** [#28](https://github.com/hungtmh/HW02-Domain_Testing/issues/28) - [FR-02] [BUG-002] Account lockout duration is 180 seconds instead of 30 seconds
- **BUG-FR02-003:** [#29](https://github.com/hungtmh/HW02-Domain_Testing/issues/29) - [FR-02] [BUG-003] Login email field does not use type="email"
- **BUG-FR07-001:** [#30](https://github.com/hungtmh/HW02-Domain_Testing/issues/30) - [FR-07] [BUG-001] Adding same product creates duplicate rows
- **BUG-FR07-002:** [#31](https://github.com/hungtmh/HW02-Domain_Testing/issues/31) - [FR-07] [BUG-002] Cart quantity has no +/- controls
- **BUG-FR07-003:** [#32](https://github.com/hungtmh/HW02-Domain_Testing/issues/32) - [FR-07] [BUG-003] Delete cart item does not show confirmation dialog
- **BUG-FR07-004:** [#33](https://github.com/hungtmh/HW02-Domain_Testing/issues/33) - [FR-07] [BUG-004] Cart total label is wrong
- **BUG-FR07-005:** [#34](https://github.com/hungtmh/HW02-Domain_Testing/issues/34) - [FR-07] [BUG-005] Empty cart has no illustration
- **BUG-FR16-001:** [#35](https://github.com/hungtmh/HW02-Domain_Testing/issues/35) - [FR-16] [BUG-001] Normal user can call admin product import API
- **BUG-FR16-002:** [#36](https://github.com/hungtmh/HW02-Domain_Testing/issues/36) - [FR-16] [BUG-002] Product import is not atomic when a row is invalid
- **BUG-FR16-003:** [#37](https://github.com/hungtmh/HW02-Domain_Testing/issues/37) - [FR-16] [BUG-003] Product import accepts negative price
- **BUG-FR16-004:** [#38](https://github.com/hungtmh/HW02-Domain_Testing/issues/38) - [FR-16] [BUG-004] CSV parser does not support quoted commas
- **BUG-MOB-001:** [#39](https://github.com/hungtmh/HW02-Domain_Testing/issues/39) - [Mobile-Product-Listing] [BUG-001] Mobile API URL is hard-coded
- **BUG-MOB-002:** [#40](https://github.com/hungtmh/HW02-Domain_Testing/issues/40) - [Mobile-Product-Listing] [BUG-002] Search query is not URL-encoded
- **BUG-MOB-003:** [#41](https://github.com/hungtmh/HW02-Domain_Testing/issues/41) - [Mobile-Product-Listing] [BUG-003] Product search has no empty state
- **BUG-MOB-004:** [#42](https://github.com/hungtmh/HW02-Domain_Testing/issues/42) - [Mobile-Product-Listing] [BUG-004] Product images use resizeMode="stretch"

Evidence chính thức vẫn nằm trong các thư mục `reports/*_bugs/` và được link trong từng issue.
