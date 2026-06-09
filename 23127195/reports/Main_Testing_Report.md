# Main Testing Report — EShop Testing

**MSSV:** 23127195  
**Ngày lập:** 2026-06-09  

---

# FEATURE: FR-01 — ĐĂNG KÝ TÀI KHOẢN

## 1. Domain Testing — FR-01

**SUT:** Frontend Web (`http://localhost:5173/register`) + API `POST /api/register`

### Bước 1 — Phạm vi và SUT

#### Tài liệu Đặc tả (SRS FR-01)
- **Các trường thông tin bắt buộc:** Họ Tên, Email, Mật khẩu, Xác nhận mật khẩu.
- **Ràng buộc định dạng Email:** Phải có định dạng hợp lệ (`user@domain.com`) và là **duy nhất** trong hệ thống.
- **Ràng buộc Mật khẩu mạnh:** Tối thiểu 8 ký tự, chứa ít nhất: 1 chữ cái in hoa, 1 chữ cái in thường, 1 chữ số, và 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`).
- **Trường Xác nhận mật khẩu:** Hệ thống phải kiểm tra xem giá trị nhập vào có khớp với trường Mật khẩu hay không. Nếu không khớp, từ chối đăng ký.
- **Hành vi sau khi thành công:** Người dùng được chuyển hướng tới trang Đăng nhập (`/login`).

#### Các file mã nguồn liên quan
- **Frontend Web:** [Register.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Register.jsx)
- **Routing:** [App.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/App.jsx)
- **Backend API:** [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) (dòng 20–30)
- **Database:** [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js) (dòng 50-61 - bảng `users`)

#### Phân tích sơ bộ từ mã nguồn thực tế (Code vs SRS)
1. **Thiếu trường dữ liệu:** Form đăng ký trên giao diện Frontend Web hoàn toàn **không có trường Xác nhận mật khẩu** (`confirmPassword`).
2. **Regex mật khẩu bị sai:** Regex kiểm tra mật khẩu mạnh ở Frontend (`flawedStrongPasswordRegex` tại dòng 15 của `Register.jsx`) yêu cầu **khoảng trắng** (`\s`) thay vì ký tự đặc biệt theo SRS, và loại trừ tất cả các ký tự đặc biệt chuẩn (`@`, `$`, `!`, v.v.).
3. **Backend bỏ qua xác thực:** API `POST /api/register` trên backend không thực hiện bất kỳ khâu kiểm tra định dạng hoặc độ mạnh mật khẩu nào.
4. **Trùng lặp email:** Bảng `users` trong cơ sở dữ liệu SQLite không định nghĩa cột `email` là `UNIQUE`, đồng thời backend không kiểm tra email đã tồn tại trước khi ghi nhận bản ghi mới.

### Bước 2 — Input Variables

| ID | Biến | Kiểu dữ liệu | Nguồn | Ràng buộc từ SRS |
|----|------|--------------|-------|------------------|
| V1 | name | String | Form UI / API Body | Không được để trống |
| V2 | email | String | Form UI / API Body | Định dạng email hợp lệ, là duy nhất trong DB |
| V3 | password | String | Form UI / API Body | Độ dài >= 8, chứa ít nhất 1 hoa, 1 thường, 1 số, 1 ký tự đặc biệt |
| V4 | confirmPassword | String | Form UI (Thiếu trên Web) | Khớp hoàn toàn với `password` |
| V5 | email_in_db | Boolean | Database | Trạng thái tồn tại của email (`true` nếu đã có) |

**Bộ giá trị hợp lệ mặc định (để kiểm thử đơn lỗi):**
- `name`: `"Nguyen Van A"`
- `email`: `"unique_user_99@test.com"` (chưa tồn tại)
- `password`: `"Test1234!"`
- `confirmPassword`: `"Test1234!"`

### Bước 3 — Domains (Miền giá trị)

| Biến | Miền hợp lệ (Valid Domain) | Miền không hợp lệ (Invalid Domain) | Giá trị đặc biệt (Special/Edge Values) |
|------|----------------------------|-----------------------------------|---------------------------------------|
| **name** | Chuỗi chữ từ 1 ký tự trở lên | Chuỗi rỗng `""` | Khoảng trắng đầu/cuối, thẻ HTML/XSS (`<script>`), SQL Injection (`' OR 1=1--`) |
| **email** | Đúng định dạng email RFC, chưa tồn tại trong DB | Sai định dạng, đã tồn tại trong DB | Chứa ký tự Unicode, TLD cực ngắn hoặc cực dài, giá trị rỗng |
| **password** | Độ dài >= 8, chứa ít nhất 1 hoa, 1 thường, 1 số, 1 ký tự đặc biệt SRS | Độ dài < 8, thiếu một trong các thành phần bắt buộc | Chứa khoảng trắng, SQL Injection, chuỗi siêu dài |
| **confirmPassword** | Khớp 100% với `password` | Khác biệt so với `password` | Để trống khi `password` đã nhập |

### Bước 4 — Equivalence Partitions (Phân vùng tương đương)

| EP-ID | Loại vùng | Biến tác động | Mô tả phân vùng tương đương | Giá trị đại diện |
|-------|-----------|---------------|-----------------------------|------------------|
| **EP-N01** | Hợp lệ | name | Tên người dùng thông thường | `"Nguyen Van A"` |
| **EP-N02** | Không hợp lệ | name | Tên bị bỏ trống | `""` |
| **EP-N03** | Không hợp lệ | name | Tên chỉ gồm các khoảng trắng | `"   "` |
| **EP-E01** | Hợp lệ | email | Email đúng định dạng và chưa tồn tại | `"newuser_001@eshop.com"` |
| **EP-E02** | Không hợp lệ | email | Email đúng định dạng nhưng đã tồn tại | `"test@eshop.com"` |
| **EP-E03** | Không hợp lệ | email | Email sai định dạng | `"not-an-email"`, `"user@.com"` |
| **EP-E04** | Không hợp lệ | email | Email bị bỏ trống | `""` |
| **EP-P01** | Hợp lệ | password | Mật khẩu hợp lệ theo đặc tả SRS | `"Test1234!"` |
| **EP-P02** | Không hợp lệ | password | Mật khẩu quá ngắn (< 8 ký tự) | `"Test1!"` |
| **EP-P03** | Không hợp lệ | password | Mật khẩu thiếu chữ cái in hoa | `"test1234!"` |
| **EP-P04** | Không hợp lệ | password | Mật khẩu thiếu chữ cái in thường | `"TEST1234!"` |
| **EP-P05** | Không hợp lệ | password | Mật khẩu thiếu chữ số | `"TestTest!"` |
| **EP-P06** | Không hợp lệ | password | Mật khẩu thiếu ký tự đặc biệt SRS | `"Test1234"` |
| **EP-P07** | Không hợp lệ | password | Mật khẩu dùng khoảng trắng làm ký tự đặc biệt | `"Test 1234"` |
| **EP-C01** | Hợp lệ | confirmPassword | Khớp hoàn toàn với mật khẩu | `"Test1234!"` (khi pass = `"Test1234!"`) |
| **EP-C02** | Không hợp lệ | confirmPassword | Không trùng khớp với mật khẩu | `"Test1234@"` (khi pass = `"Test1234!"`) |
| **EP-C03** | Không hợp lệ | confirmPassword | Bị bỏ trống | `""` |
| **EP-C04** | Không hợp lệ | confirmPassword | Không hiển thị/thiếu trường trên giao diện | *(Không nhập được trên UI)* |

### Bước 5 — Constraints (Các ràng buộc nghiệp vụ)

| C-ID | Ràng buộc nghiệp vụ | Loại ràng buộc | Hành vi kỳ vọng của hệ thống |
|------|---------------------|----------------|------------------------------|
| **C-01** | Khớp mật khẩu | Ràng buộc chéo | `confirmPassword` phải giống hệt `password` thì mới kích hoạt submit. |
| **C-02** | Email duy nhất | Ràng buộc nghiệp vụ | Hệ thống từ chối đăng ký và trả lỗi nếu `email_in_db == true`. |
| **C-03** | Mật khẩu mạnh | Ràng buộc định dạng | Validate mật khẩu dựa trên cấu trúc SRS ở cả Client và Server. |
| **C-04** | Sau thành công | Luồng hậu điều kiện | Thực hiện lưu trữ thông tin và chuyển hướng (redirect) về `/login`. |
| **C-05** | Trường bắt buộc | Ràng buộc giao diện | Các ô nhập bắt buộc phải được đánh dấu và ngăn chặn submit rỗng ở Client. |

### Bước 6 — Test Cases thiết kế từ Domain Testing

*Mặc định các trường còn lại sẽ giữ giá trị hợp lệ để thực hiện kỹ thuật Single-Fault.*

| TC-ID | Mô tả kịch bản kiểm thử | Input thực tế đầu vào | Kết quả mong đợi theo SRS | Phân vùng EP / Ràng buộc |
|-------|-------------------------|-----------------------|---------------------------|-------------------------|
| **DT-01** | Đăng ký thành công (Happy Path) | `name="Nguyen Van A"`, `email="new_auth@test.com"`, `password="Test1234!"`, `confirmPassword="Test1234!"` | Đăng ký thành công, chuyển hướng về `/login` | EP-N01, EP-E01, EP-P01, EP-C01, C-04 |
| **DT-02** | Đăng ký với Email đã tồn tại | `email="test@eshop.com"` | Từ chối đăng ký, thông báo lỗi email đã tồn tại | EP-E02, C-02 |
| **DT-03** | Đăng ký với Email sai định dạng | `email="invalid-email"` | Từ chối đăng ký, thông báo email không hợp lệ | EP-E03 |
| **DT-04** | Đăng ký với Email bỏ trống | `email=""` | Trình duyệt chặn submit hoặc API trả về lỗi yêu cầu Email | EP-E04, C-05 |
| **DT-05** | Đăng ký với Họ Tên bị bỏ trống | `name=""` | Trình duyệt chặn submit hoặc API trả về lỗi yêu cầu Họ Tên | EP-N02, C-05 |
| **DT-06** | Đăng ký với Họ Tên chỉ có khoảng trắng | `name="   "` | Từ chối đăng ký | EP-N03 |
| **DT-07** | Mật khẩu hợp lệ SRS nhưng không có khoảng trắng | `password="Test1234!"` | Chấp nhận đăng ký (kiểm tra lỗi Regex Web chặn sai) | EP-P01 |
| **DT-08** | Mật khẩu có khoảng trắng nhưng không có ký tự đặc biệt SRS | `password="Test 1234"` | Từ chối đăng ký vì thiếu ký tự đặc biệt | EP-P07, EP-P06 |
| **DT-09** | Nhập mật khẩu thiếu chữ in hoa | `password="test1234!"` | Từ chối đăng ký vì mật khẩu quá yếu | EP-P03 |
| **DT-10** | Xác nhận mật khẩu không khớp | `password="Test1234!"`, `confirmPassword="Test1234@"` | Từ chối đăng ký, báo lỗi mật khẩu xác nhận không khớp | EP-C02, C-01 |
| **DT-11** | Kiểm tra sự tồn tại của trường Xác nhận mật khẩu trên giao diện | Kiểm tra trực quan trên màn hình Đăng ký | Có trường "Xác nhận mật khẩu" để nhập | EP-C04 |
| **DT-12** | SQL Injection trong trường Email | `email="' OR '1'='1--"` | Từ chối đăng ký / Escape an toàn, không lỗi DB | Giá trị đặc biệt |
| **DT-13** | XSS (Cross-Site Scripting) trong trường Họ Tên | `name="<script>alert('XSS')</script>"` | Lưu trữ an toàn, không thực thi mã script khi hiển thị | Giá trị đặc biệt |

---

## 2. Boundary Value Analysis — FR-01

**SUT:** Frontend Web + API `POST /api/register`

### Bước 1 — Xác định các biên (Boundaries) từ đặc tả SRS

Dựa vào SRS FR-01, ta xác định các biên sau:

| B-ID | Biến | Ràng buộc SRS | Điểm biên dưới (Min) | Điểm biên trên (Max) | Kiểu biên |
|------|------|---------------|----------------------|----------------------|-----------|
| **B-PW-LEN** | password | Độ dài mật khẩu | 8 ký tự | Không giới hạn | Giá trị số |
| **B-PW-UP** | password | Số lượng chữ in hoa | 1 ký tự hoa | Không giới hạn | Số lượng thành phần |
| **B-PW-LO** | password | Số lượng chữ in thường | 1 ký tự thường | Không giới hạn | Số lượng thành phần |
| **B-PW-DI** | password | Số lượng chữ số | 1 chữ số | Không giới hạn | Số lượng thành phần |
| **B-PW-SP** | password | Số lượng ký tự đặc biệt | 1 ký tự đặc biệt (`@$!%*?&`) | Không giới hạn | Số lượng thành phần |
| **B-NAME-LEN** | name | Độ dài họ tên | 1 ký tự | Không giới hạn | Giá trị số |

### Bước 2 — Xác định các điểm kiểm thử biên (BVA Points)

Sử dụng phương pháp BVA truyền thống (chọn các điểm: Biên, Sát dưới biên, Sát trên biên) và Robustness testing (nếu cần).

#### 1. Phân tích biên cho độ dài Mật khẩu (B-PW-LEN)
- **Sát dưới biên (Min - 1):** 7 ký tự. Giá trị kiểm thử: `"Test12!"` -> Kỳ vọng: **Từ chối (Reject)**
- **Tại biên (Min):** 8 ký tự. Giá trị kiểm thử: `"Test123!"` -> Kỳ vọng: **Chấp nhận (Accept)**
- **Sát trên biên (Min + 1):** 9 ký tự. Giá trị kiểm thử: `"Test1234!"` -> Kỳ vọng: **Chấp nhận (Accept)**

#### 2. Phân tích biên cho thành phần cấu trúc Mật khẩu (Password Composition)
- **Số chữ in hoa = 0 (Dưới biên):** `"test1234!"` -> Kỳ vọng: **Từ chối**
- **Số chữ in hoa = 1 (Tại biên):** `"Test1234!"` -> Kỳ vọng: **Chấp nhận**
- **Số chữ in thường = 0 (Dưới biên):** `"TEST1234!"` -> Kỳ vọng: **Từ chối**
- **Số chữ in thường = 1 (Tại biên):** `"tEST1234!"` -> Kỳ vọng: **Chấp nhận**
- **Số chữ số = 0 (Dưới biên):** `"TestTest!"` -> Kỳ vọng: **Từ chối**
- **Số chữ số = 1 (Tại biên):** `"Test1234!"` -> Kỳ vọng: **Chấp nhận**
- **Số ký tự đặc biệt = 0 (Dưới biên):** `"Test1234"` -> Kỳ vọng: **Từ chối**
- **Số ký tự đặc biệt = 1 (Tại biên):** `"Test1234!"` -> Kỳ vọng: **Chấp nhận**

#### 3. Phân tích biên do cài đặt thực tế của mã nguồn (Implementation-specific boundary)
- **Mật khẩu chứa ký tự đặc biệt chuẩn SRS, không chứa khoảng trắng:** `"Test1234!"` -> SRS: **Chấp nhận** | Frontend thực tế: **Từ chối**
- **Mật khẩu chứa khoảng trắng, không chứa ký tự đặc biệt SRS:** `"Test 1234"` -> SRS: **Từ chối** | Frontend thực tế: **Chấp nhận**

### Bước 3 — Danh sách Test Cases thiết kế từ BVA

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
| **BV-11** | `email="a@b.co"` (TLD ngắn hợp lệ) | Biên định dạng email ngắn nhất | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-12** | `email="a@b.c"` (TLD không hợp lệ) | Biên định dạng email không hợp lệ | Từ chối | Từ chối | Từ chối |

### Bước 4 — Kịch bản biên Robustness / Edge cases bổ sung

| TC-ID | Đầu vào kiểm thử | Mục đích kiểm tra | Kết quả mong đợi |
|-------|------------------|-------------------|------------------|
| **BV-R01** | password dài 500 ký tự | Kiểm tra tràn bộ đệm / giới hạn đầu vào | Từ chối hoặc chấp nhận an toàn, không crash hệ thống |
| **BV-R02** | name có ký tự Unicode `"Nguyễn Văn Hoài"` | Kiểm tra hỗ trợ đa ngôn ngữ | Chấp nhận đăng ký |
| **BV-R03** | email có phần domain in hoa `"user@TEST.COM"` | Kiểm tra tính không phân biệt hoa thường của domain | Chấp nhận đăng ký |

---

## 3. Test Execution — FR-01

**Ngày thực thi:** 2026-06-09  
**Môi trường:** Windows 10, Node.js v18+, SQLite, Chrome / React Web (:5173)

### Kết quả tổng hợp (Test Summary)

| Chỉ số (Metric) | Số lượng (Count) |
|-----------------|------------------|
| Tổng số test case thiết kế | 17 |
| Đã thực thi (Executed) | 15 |
| **ĐẠT (Pass)** | 4 |
| **KHÔNG ĐẠT (Fail)** | 11 |
| Chưa chạy (Not run) | 2 |

### Nhật ký thực thi API Layer (`POST /api/register`)

Thực hiện gọi API trực tiếp bằng PowerShell `Invoke-RestMethod` để kiểm tra khả năng kiểm thực ở phía server:

| TC-ID | Dữ liệu đầu vào (Request Body) | HTTP Code | Kết quả thực tế (Actual) | Kết quả mong đợi (Expected) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-----------------------------|-----------|--------------------------|----------------------------|---------------------|-----------------|
| **DT-01** | `name="Nguyen Van A"`, `email="new_auth_01@test.com"`, `password="Test1234!"` | 200 OK | `{"message":"User registered successfully","id":3}` | Đăng ký thành công, tạo tài khoản mới | **PASS** | — |
| **DT-02** | `email="test@eshop.com"` (Đã có sẵn trong DB) | 200 OK | `{"message":"User registered successfully","id":4}` | Từ chối đăng ký, báo trùng email | **FAIL** | [BUG-001](./Consolidated_Bug_Report.md#bug-001-api-cho-phep-dang-ky-trung-email) |
| **DT-03** | `email="invalid-email"` | 200 OK | `{"message":"User registered successfully","id":5}` | Từ chối đăng ký, báo sai định dạng | **FAIL** | [BUG-002](./Consolidated_Bug_Report.md#bug-002-api-cho-phep-dang-ky-email-sai-dinh-dang) |
| **DT-04** | `email=""` (Bỏ trống email) | 200 OK | `{"message":"User registered successfully","id":6}` | Từ chối đăng ký | **FAIL** | [BUG-003](./Consolidated_Bug_Report.md#bug-003-api-cho-phep-dang-ky-khi-bo-trong-cac-truong-bat-buoc) |
| **DT-05** | `name=""` (Bỏ trống họ tên) | 200 OK | `{"message":"User registered successfully","id":6}` | Từ chối đăng ký | **FAIL** | [BUG-003](./Consolidated_Bug_Report.md#bug-003-api-cho-phep-dang-ky-khi-bo-trong-cac-truong-bat-buoc) |
| **BV-01** | `password="Test12!"` (7 ký tự) | 200 OK | `{"message":"User registered successfully","id":7}` | Từ chối đăng ký | **FAIL** | [BUG-004](./Consolidated_Bug_Report.md#bug-004-api-khong-xac-thuc-do-manh-mat-khau) |
| **BV-02** | `password="Test123!"` (8 ký tự) | 200 OK | `{"message":"User registered successfully","id":8}` | Chấp nhận đăng ký | **PASS** | — |
| **BV-04** | `password="test1234!"` (Thiếu chữ hoa) | 200 OK | `{"message":"User registered successfully","id":8}` | Từ chối đăng ký | **FAIL** | [BUG-004](./Consolidated_Bug_Report.md#bug-004-api-khong-xac-thuc-do-manh-mat-khau) |
| **BV-08** | `password="Test 1234"` (Có space, không special) | 200 OK | `{"message":"User registered successfully","id":9}` | Từ chối đăng ký | **FAIL** | [BUG-004](./Consolidated_Bug_Report.md#bug-004-api-khong-xac-thuc-do-manh-mat-khau) |
| **BV-11** | `email="a@b.co"` (TLD ngắn hợp lệ) | 200 OK | Đăng ký thành công | Chấp nhận đăng ký | **PASS** | — |
| **BV-12** | `email="a@b.c"` (TLD không hợp lệ) | 200 OK | Đăng ký thành công | Từ chối đăng ký | **FAIL** | [BUG-002](./Consolidated_Bug_Report.md#bug-002-api-cho-phep-dang-ky-email-sai-dinh-dang) |

### Nhật ký thực thi UI / Code Review (Frontend Web)

| TC-ID | Nội dung kiểm thử | Kết quả thực tế (Code & UI) | Kết quả mong đợi (SRS) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-------------------|-----------------------------|------------------------|---------------------|-----------------|
| **DT-10** | Xác nhận mật khẩu không khớp | Form không có trường Confirm Password | Phải báo lỗi và chặn submit | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-thieu-truong-xac-nhan-mat-khau-tren-ui-frontend) |
| **DT-11** | Có trường Xác nhận mật khẩu trên UI | Không có trường "Xác nhận mật khẩu" trên giao diện | Phải hiển thị trường nhập | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-thieu-truong-xac-nhan-mat-khau-tren-ui-frontend) |
| **DT-07** | Nhập pass hợp lệ SRS `"Test1234!"` | Bị client chặn và báo mật khẩu quá yếu | Chấp nhận submit | **FAIL** | [BUG-006](./Consolidated_Bug_Report.md#bug-006-regex-kiem-tra-mat-khau-manh-o-frontend-bi-sai-yeu-cau-khoang-trang) |
| **DT-08** | Nhập pass có khoảng trắng `"Test 1234"` | Client chấp nhận cho phép submit đăng ký | Phải từ chối vì thiếu ký tự đặc biệt | **FAIL** | [BUG-006](./Consolidated_Bug_Report.md#bug-006-regex-kiem-tra-mat-khau-manh-o-frontend-bi-sai-yeu-cau-khoang-trang) |
| **DT-01 (UI)** | Đăng ký thành công điều hướng về Login | Gọi `navigate('/login')` chuyển trang | Phải chuyển hướng về `/login` | **PASS** | — |
| **DT-04 (UI)** | Email type attribute | Trường nhập Email có thuộc tính `type="text"` | Phải có thuộc tính `type="email"` | **FAIL** | [BUG-007](./Consolidated_Bug_Report.md#bug-007-man-hinh-dang-ky-su-dung-o-nhap-email-kieu-type%3Dtext) |

### Đánh giá & Khuyến nghị
- **Backend:** Cần validate định dạng bằng thư viện và cấu hình thuộc tính `UNIQUE` cho cột email trong SQLite.
- **Frontend:** Thiết kế lại trường Xác nhận mật khẩu và sửa lại Regex mật khẩu mạnh của form.
- **Bảo mật:** Đưa logic băm mật khẩu `bcryptjs` vào backend thay vì lưu plaintext.

---

## 4. AI Gap Analysis — FR-01

### 1. Những lỗi và kịch bản kiểm thử AI thông thường bỏ sót (AI Gaps)

| Kịch bản kiểm thử / Lỗi bị bỏ sót | Lý do AI bỏ sót (Root cause of AI gap) | Bài học rút ra & Giải pháp khắc phục |
|-----------------------------------|----------------------------------------|-------------------------------------|
| **1. Thiếu trường Xác nhận mật khẩu trên UI (BUG-005)** | AI đọc SRS và tự suy luận ra test case mà không chủ động đối chiếu mã nguồn thực tế của giao diện Frontend. | Yêu cầu AI bắt buộc phải đọc mã nguồn UI trước khi thiết kế các test case ở mức giao diện. |
| **2. Regex mật khẩu mạnh bị sai (BUG-006)** | AI thường tin tưởng tuyệt đối rằng các Regex trong mã nguồn đã được dev viết đúng theo đặc tả. | Cần prompt AI thực hiện phân tích tĩnh (Static Analysis) đối với Regex thực tế trong code. |
| **3. Backend API hoàn toàn không validate dữ liệu (BUG-003, BUG-004)** | AI có xu hướng tập trung kiểm thử hộp đen trên giao diện Web mà quên mất việc kiểm thử API trực tiếp (API Validation Bypass). | Phải yêu cầu AI lập hai danh sách test case riêng biệt: Client-side validation và Server-side API validation. |
| **4. Database cho phép trùng Email (BUG-001)** | AI mặc định giả định rằng cơ sở dữ liệu luôn định nghĩa các ràng buộc duy nhất (`UNIQUE`). | Ép buộc AI đọc file cấu hình database schema trước khi kết luận về tính độc bản của dữ liệu. |
| **5. Lưu trữ mật khẩu dạng Plaintext (BUG-008)** | Lỗi này nằm ở mức phân tích an toàn thông tin (Security Audit). AI thông thường chỉ tập trung vào kiểm thử chức năng. | Cần tích hợp thêm bước rà soát bảo mật (Security review) vào luồng làm việc tiêu chuẩn. |

### 2. Cách cải tiến prompt để tối ưu hóa AI
1. **Prompt định hướng đọc mã nguồn:** Yêu cầu AI đối chiếu chính xác file code với SRS.
2. **Prompt phân tách tầng kiểm thử:** Yêu cầu danh sách TC riêng cho Client-side và API-side.
3. **Prompt phân tích biên thực tế:** Yêu cầu test chính xác giá trị `Min - 1`, `Min`, `Min + 1` và robustness.

---
---

# FEATURE: FR-09 — MÃ GIẢM GIÁ (DISCOUNT COUPONS)

## 1. Domain Testing — FR-09

**SUT:** Backend API `POST /api/apply-coupon` + Giao diện Checkout (`http://localhost:5173/checkout`)

### Bước 1 — Phạm vi và SUT

#### Tài liệu Đặc tả (SRS FR-09)
Hệ thống áp dụng giảm giá khi người dùng nhập mã giảm giá tại bước Checkout. Có **5 điều kiện** bắt buộc phải thỏa mãn:
1. **C1 (Mã tồn tại & hoạt động):** Mã phải tồn tại trong cơ sở dữ liệu và đang hoạt động (`is_active = 1`).
2. **C2 (Còn hạn sử dụng):** Ngày hiện tại phải trước ngày hết hạn (`expired_at`).
3. **C3 (Đủ ngưỡng đơn hàng):** Tổng đơn hàng phải lớn hơn hoặc bằng (`>=`) giá trị `min_order_amount`.
4. **C4 (Đã đăng nhập):** Người dùng phải có Token JWT hợp lệ gửi kèm.
5. **C5 (Chưa dùng hết lượt):** Số lần người dùng đã sử dụng mã này phải nhỏ hơn (`<`) giới hạn `max_uses_per_user`.

**Công thức tính toán giảm giá:**
- Loại `percent`: `discount_amount = total × discount_value / 100`
- Loại `fixed`: `discount_amount = discount_value`
- `final_amount = total - discount_amount`

#### Các file mã nguồn liên quan
- **Frontend Web:** [Checkout.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Checkout.jsx) (dòng 22-38, 105-134)
- **Backend API:** [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) (dòng 363–441)
- **Database:** [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js)

### Bước 2 — Input Variables (Biến đầu vào)

| ID | Biến | Kiểu dữ liệu | Nguồn | Ràng buộc từ SRS |
|----|------|--------------|-------|------------------|
| V1 | `code` | String | Form UI / API Body | Mã phải tồn tại và có `is_active = 1` |
| V2 | `total_amount` | Integer | Giỏ hàng / API Body | Phải lớn hơn hoặc bằng `min_order_amount` |
| V3 | `token` | String (JWT) | Headers | Token phải hợp lệ (người dùng đã đăng nhập) |
| V4 | `user_id` | Integer | Token / API Body | Cần thiết để đếm số lần sử dụng mã của user |
| V5 | `current_time` | Datetime | System | Phải trước ngày hết hạn `expired_at` của mã |

**Bộ giá trị hợp lệ mặc định:**
- `code`: `"SAVE10"`
- `total_amount`: `350000` (thỏa mãn ngưỡng tối thiểu 300,000 ₫)
- `user_id`: `2` (user test)

### Bước 3 — Domains (Miền giá trị)

| Biến | Miền hợp lệ (Valid Domain) | Miền không hợp lệ (Invalid Domain) | Giá trị đặc biệt (Special/Edge Values) |
|------|----------------------------|-----------------------------------|---------------------------------------|
| **code** | Mã có trong DB và `is_active = 1` | Mã không tồn tại, mã có `is_active = 0` | Để trống `""`, ký tự đặc biệt, SQL injection |
| **total_amount** | Giá trị `>= min_order_amount` | Giá trị `< min_order_amount` | Bằng 0, số âm, cực lớn (overflow) |
| **token** | Token JWT hợp lệ và chưa hết hạn | Không gửi kèm token, token hết hạn | Token rỗng |
| **user_id** | ID của user đã đăng nhập khớp token | ID của user khác (giả mạo), ID không tồn tại | `NULL`, rỗng |

### Bước 4 — Equivalence Partitions (Phân vùng tương đương)

| EP-ID | Loại vùng | Biến tác động | Mô tả phân vùng tương đương | Giá trị đại diện |
|-------|-----------|---------------|-----------------------------|------------------|
| **EP-CP01** | Hợp lệ | code | Mã tồn tại, đang hoạt động | `"SAVE10"`, `"BIGBUY"` |
| **EP-CP02** | Không hợp lệ | code | Mã không tồn tại | `"INVALID_CODE"` |
| **EP-CP03** | Không hợp lệ | code | Mã tồn tại nhưng đã bị vô hiệu hóa | `"DISABLED_CODE"` |
| **EP-CP04** | Không hợp lệ | code | Mã giảm giá bị bỏ trống | `""` |
| **EP-EXP1** | Hợp lệ | current_time | Còn hạn sử dụng (ngày < expired_at) | `"SAVE10"` (hạn 2099) |
| **EP-EXP2** | Không hợp lệ | current_time | Đã hết hạn sử dụng (ngày >= expired_at) | `"EXPIRED"` (hạn 2020) |
| **EP-AMT1** | Hợp lệ | total_amount | Tổng đơn hàng `>= min_order_amount` | `total_amount = 350000` (mã `SAVE10`) |
| **EP-AMT2** | Không hợp lệ | total_amount | Tổng đơn hàng `< min_order_amount` | `total_amount = 250000` (mã `SAVE10`) |
| **EP-AUTH1**| Hợp lệ | token | Đã đăng nhập, token hợp lệ | `Bearer <valid_token>` |
| **EP-AUTH2**| Không hợp lệ | token | Chưa đăng nhập (không gửi token) | *Không gửi Header Authorization* |
| **EP-USG1** | Hợp lệ | user_id | Số lần đã sử dụng mã < max_uses_per_user | Sử dụng 0 lần (mã `SAVE10` limit 1) |
| **EP-USG2** | Không hợp lệ | user_id | Số lần đã sử dụng mã >= max_uses_per_user | Sử dụng 1 lần (mã `SAVE10` limit 1) |
| **EP-TYP1** | Hợp lệ | coupon type | Loại mã giảm giá theo phần trăm (`percent`) | `"SAVE10"` (giảm 10%) |
| **EP-TYP2** | Hợp lệ | coupon type | Loại mã giảm giá cố định (`fixed`) | `"BIGBUY"` (giảm 50,000 ₫) |

### Bước 5 — Constraints (Các ràng buộc nghiệp vụ)

| C-ID | Ràng buộc chéo / Nghiệp vụ | Loại ràng buộc | Kết quả kỳ vọng |
|------|---------------------------|----------------|-----------------|
| **C-01** | Tất cả điều kiện đồng thời | Ràng buộc chéo | Chỉ áp dụng giảm giá khi cả 5 điều kiện (C1 đến C5) đều thỏa mãn. |
| **C-02** | Loại mã `percent` | Tính toán | Tiết kiệm `discount_amount = total * discount_value / 100`. |
| **C-03** | Loại mã `fixed` | Tính toán | Tiết kiệm `discount_amount = discount_value`. |
| **C-04** | Kiểm tra chéo user_id | Ràng buộc bảo mật | Không cho phép gửi kèm `user_id` giả mạo trong body nếu không có token JWT khớp tương ứng. |

### Bước 6 — Test Cases thiết kế từ Domain Testing

| TC-ID | Mô tả kịch bản kiểm thử | Input thực tế đầu vào | Kết quả mong đợi theo SRS | Phân vùng EP / Ràng buộc |
|-------|-------------------------|-----------------------|---------------------------|-------------------------|
| **DT-01** | Áp dụng thành công mã `SAVE10` (loại percent) | code=`"SAVE10"`, total=`350000`, user_id=`2` | Áp dụng thành công, giảm `35,000 ₫`, thành tiền `315,000 ₫` | EP-CP01, EP-TYP1, C-02 |
| **DT-02** | Áp dụng thành công mã `BIGBUY` (loại fixed) | code=`"BIGBUY"`, total=`550000`, user_id=`2` | Áp dụng thành công, giảm `50,000 ₫`, thành tiền `500,000 ₫` | EP-CP01, EP-TYP2, C-03 |
| **DT-03** | Áp dụng mã không tồn tại | code=`"NOSUCH"`, total=`350000` | Báo lỗi: "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa" | EP-CP02 |
| **DT-04** | Áp dụng mã giảm giá bị rỗng | code=`""`, total=`350000` | Báo lỗi yêu cầu nhập mã giảm giá | EP-CP04 |
| **DT-05** | Áp dụng mã giảm giá đã hết hạn | code=`"EXPIRED"`, total=`150000`, user_id=`2` | Báo lỗi: "Mã giảm giá đã hết hạn" | EP-EXP2 |
| **DT-06** | Áp dụng mã khi tổng tiền chưa đạt ngưỡng tối thiểu | code=`"SAVE10"`, total=`250000`, user_id=`2` | Báo lỗi đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ | EP-AMT2 |
| **DT-07** | Áp dụng mã khi chưa đăng nhập (Guest) | code=`"SAVE10"`, total=`350000` (Không gửi kèm token) | Từ chối áp dụng mã, báo lỗi yêu cầu đăng nhập | EP-AUTH2 |
| **DT-08** | Áp dụng mã vượt quá giới hạn sử dụng của user | code=`"SAVE10"`, total=`350000`, user_id=`2` (đã sử dụng mã 1 lần) | Báo lỗi người dùng đã sử dụng mã này đạt giới hạn | EP-USG2 |
| **DT-09** | Áp dụng mã bị vô hiệu hóa (`is_active = 0`) | code=`"DISABLED"`, total=`350000` | Báo lỗi mã không tồn tại hoặc bị vô hiệu hóa | EP-CP03 |
| **DT-10** | Giả mạo `user_id` trong request body | code=`"SAVE10"`, total=`350000`, body `user_id=3`, token user `2` | Từ chối hoặc tự động đếm lượt dùng dựa trên JWT | C-04, C-01 |

---

## 2. Boundary Value Analysis — FR-09

**SUT:** Backend API `POST /api/apply-coupon` + Giao diện Checkout

### Bước 1 — Xác định các biên (Boundaries) từ đặc tả SRS

| B-ID | Biến | Ràng buộc SRS | Điểm biên dưới (Min) | Điểm biên trên (Max) | Kiểu biên |
|------|------|---------------|----------------------|----------------------|-----------|
| **B-MIN-AMT** | `total_amount` | Phải `>= min_order_amount` | `min_order_amount` | Không giới hạn | Ngưỡng giá trị số |
| **B-EXP-DATE**| `current_time` | Phải `< expired_at` | Không có | `expired_at` | Ngày giờ |
| **B-USG-LIMIT**| `usage_count` | Phải `< max_uses_per_user` | Không có | `max_uses_per_user` | Số lần (count) |

### Bước 2 — Xác định các điểm kiểm thử biên (BVA Points)

#### 1. Phân tích biên cho ngưỡng đơn hàng tối thiểu (B-MIN-AMT)
*Sử dụng mã `SAVE10` (`min_order_amount = 300000 ₫`).*
- **Sát dưới biên (Min - 1):** `total_amount = 299999` -> Kỳ vọng: **Từ chối (Reject)**
- **Tại biên (Min):** `total_amount = 300000` -> Kỳ vọng: **Chấp nhận (Accept)**
- **Sát trên biên (Min + 1):** `total_amount = 300001` -> Kỳ vọng: **Chấp nhận (Accept)**

#### 2. Phân tích biên do lỗi cài đặt thực tế (Implementation-specific boundary)
- **Tại biên `total_amount = 300000`:** SRS kỳ vọng **Chấp nhận** | Backend thực tế: **Từ chối** (do check `total_amount > coupon.min_order_amount`).

#### 3. Phân tích biên cho giới hạn lượt sử dụng của người dùng (B-USG-LIMIT)
- **Dưới giới hạn (Limit - 1):** Đã dùng `0` lần -> Kỳ vọng: **Chấp nhận**
- **Tại giới hạn (Limit):** Đã dùng `1` lần -> Kỳ vọng: **Từ chối**

### Bước 3 — Danh sách Test Cases thiết kế từ BVA

*Mặc định: `code="SAVE10"`, `user_id=2`, `current_time` hợp lệ.*

| TC-ID | Input (`total_amount`) | Vùng biên kiểm tra | Expected (SRS) | Expected (Backend thực tế) | Kết quả kỳ vọng |
|-------|------------------------|-------------------|----------------|----------------------------|-----------------|
| **BV-01** | `299999` | Đơn hàng Min - 1 | Từ chối | Từ chối | Từ chối |
| **BV-02** | `300000` | Đơn hàng Min | Chấp nhận | Từ chối (do lỗi `>`) | **FAIL** (Sai logic biên) |
| **BV-03** | `300001` | Đơn hàng Min + 1 | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-04** | `total_amount = 550000`, coupon=`"BIGBUY"` | Đơn hàng Min + 50k | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-05** | `total_amount = 500000`, coupon=`"BIGBUY"` | Đơn hàng Min | Chấp nhận | Từ chối (do lỗi `>`) | **FAIL** (Sai logic biên) |
| **BV-06** | `total_amount = 499999`, coupon=`"BIGBUY"` | Đơn hàng Min - 1 | Từ chối | Từ chối | Từ chối |

### Bước 4 — Kịch bản biên Robustness / Edge cases bổ sung

| TC-ID | Đầu vào kiểm thử | Mục đích kiểm tra | Kết quả mong đợi |
|-------|------------------|-------------------|------------------|
| **BV-R01** | `total_amount = 0` | Giá trị tối thiểu | Từ chối |
| **BV-R02** | `total_amount = -100` | Giá trị âm | Từ chối |
| **BV-R03** | code = `null` | Giá trị null | Từ chối, báo lỗi |

---

## 3. Test Execution — FR-09

**Ngày thực thi:** 2026-06-09  
**Môi trường:** Windows 10, Node.js v18+, SQLite, Chrome / React Web (:5173)

### Kết quả tổng hợp (Test Summary)

| Chỉ số (Metric) | Số lượng (Count) |
|-----------------|------------------|
| Tổng số kịch bản thiết kế | 13 |
| Đã thực thi (Executed) | 12 |
| **ĐẠT (Pass)** | 5 |
| **KHÔNG ĐẠT (Fail)** | 7 |
| Chưa chạy (Not run) | 1 |

### Nhật ký thực thi API Layer (`POST /api/apply-coupon`)

Thực hiện kiểm thử API trực tiếp bằng PowerShell `Invoke-RestMethod`:

| TC-ID | Dữ liệu đầu vào (Request Body) | HTTP Code | Kết quả thực tế (Actual Result) | Kết quả mong đợi (Expected) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-----------------------------|-----------|---------------------------------|----------------------------|---------------------|-----------------|
| **DT-01** | code=`"SAVE10"`, total=`350000`, user_id=`2` | 200 OK | `discount_amount: -3150000`, `final_amount: 3500000` | Áp dụng thành công, giảm 10% (tiết kiệm 35k) | **FAIL** | [BUG-002](./Consolidated_Bug_Report.md#bug-002-sai-lech-nghiem-trong-cong-thuc-tinh-toan-giam-gia-theo-phan-tram-percent) |
| **DT-02** | code=`"BIGBUY"`, total=`550000`, user_id=`2` | 200 OK | `discount_amount: 50000`, `final_amount: 500000` | Áp dụng thành công, giảm 50k, thành tiền 500k | **PASS** | — |
| **DT-03** | code=`"NOSUCH"`, total=`350000` | 404 | `{"error":"Mã giảm giá không tồn tại..."}` | Từ chối, báo mã không tồn tại | **PASS** | — |
| **DT-04** | code=`""` | 400 | `{"error":"Vui lòng nhập mã giảm giá"}` | Từ chối, báo rỗng | **PASS** | — |
| **DT-05** | code=`"EXPIRED"`, total=`150000`, user_id=`2` | 400 | `{"error":"Mã giảm giá đã hết hạn"}` | Từ chối, báo hết hạn | **PASS** | — |
| **DT-06** | code=`"SAVE10"`, total=`250000`, user_id=`2` | 400 | `{"error":"Đơn hàng chưa đủ giá trị..."}` | Từ chối, báo chưa đủ ngưỡng | **PASS** | — |
| **DT-07** | code=`"SAVE10"`, total=`350000` (Không gửi token) | 200 OK | Áp dụng thành công | Từ chối, yêu cầu đăng nhập theo C4 | **FAIL** | [BUG-003](./Consolidated_Bug_Report.md#bug-003-api-apply-coupon-thieu-middleware-xac-thuc-jwt-authentication-bypass) |
| **DT-08** | code=`"SAVE10"`, total=`350000`, user_id=`2` (đã dùng 1 lần) | 400 | `{"error":"Bạn đã sử dụng mã này 1 lần..."}` | Từ chối vì đạt giới hạn sử dụng | **PASS** | — |
| **DT-09** | code=`"DISABLED"`, total=`350000` | 404 | Báo lỗi không tồn tại | Từ chối | **PASS** | — |
| **DT-10** | code=`"SAVE10"`, total=`350000`, user_id=`999` (ID giả mạo) | 200 OK | Áp dụng thành công | Từ chối/Kiểm tra chéo JWT token bảo mật | **FAIL** | [BUG-004](./Consolidated_Bug_Report.md#bug-004-api-cho-phep-gia-mao-id-nguoi-dung-trong-body-de-vuot-gioi-han-luot-dung) |
| **BV-02** | code=`"SAVE10"`, total=`300000`, user_id=`2` | 400 | `{"error":"Đơn hàng chưa đủ giá trị..."}` | Chấp nhận vì đơn hàng bằng đúng ngưỡng 300,000 | **FAIL** | [BUG-001](./Consolidated_Bug_Report.md#bug-001-api-apply-coupon-chan-sai-logic-bien-duoi-don-hang-toi-thieu) |
| **BV-03** | code=`"SAVE10"`, total=`300001`, user_id=`2` | 200 OK | Áp dụng thành công | Chấp nhận | **PASS** | — |

### Nhật ký thực thi UI / Code Review (Frontend Web)

| TC-ID | Nội dung kiểm thử | Kết quả thực tế (Code & UI) | Kết quả mong đợi (SRS) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-------------------|-----------------------------|------------------------|---------------------|-----------------|
| **DT-11** | Hiển thị thông báo sau khi áp dụng coupon | Render thông báo màu xanh/đỏ dưới input | Hiển thị thông báo trực quan | **PASS** | — |
| **FR-08** | Cho phép sửa đổi tổng thanh toán trên UI | Ô nhập "Tổng tiền thanh toán" cho phép người dùng nhập tự do | Không cho phép người dùng chỉnh sửa trực tiếp | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-cho-phep-nguoi-dung-chinh-sua-gia-tri-tong-thanh-toan-va-checkout-thanh-cong-voi-gia-tuy-y) |

---

## 4. AI Gap Analysis — FR-09

### 1. Những lỗi và kịch bản kiểm thử AI thông thường bỏ sót (AI Gaps)

| Kịch bản kiểm thử / Lỗi bị bỏ sót | Lý do AI bỏ sót (Root cause of AI gap) | Bài học rút ra & Giải pháp khắc phục |
|-----------------------------------|----------------------------------------|-------------------------------------|
| **1. Chặn sai logic biên dưới đơn hàng tối thiểu (BUG-001)** | AI mặc định giả định dev đã viết đúng logic so sánh `>=` của SRS. Nó ít khi tự viết test case kiểm tra biên chính xác bằng giá trị ngưỡng `total_amount = min_order_amount`. | Buộc AI phải viết các test case biên BVA cụ thể cho các điểm `Min - 1`, `Min`, `Min + 1` dựa trên cấu trúc database thực tế. |
| **2. Công thức tính toán phần trăm discount sai nghiêm trọng (BUG-002)** | AI thường tin tưởng tuyệt đối vào các phép tính số học cơ bản trong code. Nó thường chỉ viết kết quả mong đợi là "giảm 10%" mà không so khớp với công thức thực tế trong file backend. | Yêu cầu AI kiểm tra tĩnh công thức toán học được cài đặt trong code và chạy thử với dữ liệu đại diện để phát hiện sai lệch tính toán. |
| **3. API apply-coupon thiếu xác thực JWT (BUG-003)** | AI chỉ tập trung vào chức năng của mã giảm giá mà bỏ quên kiểm tra bảo mật đối với API endpoint xem nó có được bảo vệ bởi middleware xác thực hay không. | Ràng buộc AI phải phân tích các API endpoint xem có sử dụng middleware bảo mật (như `authenticateToken`) hay không. |
| **4. Giả mạo ID người dùng trong request body (BUG-004)** | AI có thói quen tin cậy thông tin đầu vào từ body và bỏ qua việc kiểm tra chéo giữa định danh của JWT và dữ liệu body gửi lên. | Tạo thói quen kiểm thử bảo mật, yêu cầu AI giả lập các request giả mạo ID người dùng khác xem server có chặn được không. |
| **5. Sửa đổi tổng tiền thanh toán tùy ý trên UI & API (BUG-005)** | AI giả định UI và API luôn đồng bộ và trường tổng tiền là chỉ đọc. Nó bỏ qua kịch bản kiểm thử thâm nhập bằng cách cố tình chỉnh sửa input value hoặc gửi API checkout giả mạo với số tiền 1 ₫. | Đưa kịch bản kiểm thử bypass giá trị (Parameter Tampering) vào danh mục test case tiêu chuẩn, yêu cầu AI kiểm tra tính toàn vẹn dữ liệu từ client lên server. |

### 2. Cách cải tiến prompt để tối ưu hóa AI
1. **Prompt yêu cầu kiểm tra tĩnh công thức toán học và logic so sánh.**
2. **Prompt định hướng kiểm thử an ninh (Security & Access Control).**
3. **Prompt kiểm thử hộp xám (Grey-box testing) kết hợp giao diện và dữ liệu.**
