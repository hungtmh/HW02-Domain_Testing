# Main Testing Report — EShop Testing

**Họ và tên:** Trần Mạnh Hùng  
**Nhóm:** Nhóm 08  
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

### 1. Các lỗi thực tế AI (Antigravity) đã bỏ sót trong các lượt chạy trước (Factual AI Gaps)

- **Lỗi thực tế bỏ sót:** Lỗ hổng bảo mật leo thang đặc quyền (Privilege Escalation) nghiêm trọng tại API cập nhật thông tin cá nhân (`PUT /api/users/me`).
- **Chi tiết:** Trong tệp [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) dòng 118-135, API cho phép cập nhật trường `role` nếu nó được truyền vào body (`if (role) { query += ", role = ?"; params.push(role); }`). Bất kỳ tài khoản người dùng bình thường nào sau khi đăng ký (FR-01) đều có thể gửi request với body `{"role": "admin"}` để tự leo thang đặc quyền lên Admin trong database.
- **Nguyên nhân bỏ sót thực tế:** AI chỉ bám sát tài liệu đặc tả SRS của luồng đăng ký (FR-01) mà không kiểm tra chéo các API tương tác tài khoản xung quanh nằm trong cùng tệp mã nguồn để xem có lỗ hổng bảo mật gián tiếp nào hay không.

### 2. Cách cải tiến prompt để tối ưu hóa AI
1. **Prompt định hướng đọc mã nguồn:** Yêu cầu AI đối chiếu chính xác file code với SRS.
2. **Prompt phân tách tầng kiểm thử:** Yêu cầu danh sách TC riêng cho Client-side và API-side.
3. **Prompt phân tích biên thực tế:** Yêu cầu test chính xác giá trị `Min - 1`, `Min`, `Min + 1` và robustness.
4. **Prompt rà soát an toàn thông tin chéo:** Yêu cầu AI kiểm tra toàn bộ API trong file backend để phát hiện lỗi phân quyền hoặc leo thang đặc quyền.


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

### 1. Các lỗi thực tế AI (Antigravity) đã bỏ sót trong các lượt chạy trước (Factual AI Gaps)

- **Lỗi thực tế bỏ sót 1:** Lỗ hổng Broken Object Level Authorization (BOLA) nghiêm trọng tại API lấy thông tin đơn hàng (`GET /api/orders/:id`).
  - **Chi tiết:** Trong tệp [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) dòng 344-349, API này hoàn toàn thiếu middleware `authenticateToken`. Bất kỳ người dùng vãng lai nào (không cần đăng nhập) cũng có thể gửi yêu cầu GET tới `/api/orders/<ID>` để đọc thông tin chi tiết đơn hàng (bao gồm họ tên, địa chỉ giao hàng và giá trị tiền) của mọi đơn hàng trong hệ thống.
- **Lỗi thực tế bỏ sót 2:** Logic chuyển đổi trạng thái đơn hàng bị sai nghiêm trọng tại API Admin cập nhật trạng thái đơn hàng (`PUT /api/admin/orders/:id/status`).
  - **Chi tiết:** Trong tệp [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) dòng 550-551, backend cho phép chuyển đổi từ trạng thái Đã hủy (`canceled`) trực tiếp sang trạng thái Đã giao (`delivered`) thông qua dòng code: `if (currentStatus === "canceled" && status === "delivered") isValidTransition = true;`. Đây là lỗi logic nghiệp vụ nghiêm trọng.
- **Nguyên nhân bỏ sót thực tế:** AI chỉ thiết kế các test case cho luồng checkout và mã giảm giá chính xác theo đặc tả SRS FR-09 mà không thực hiện kiểm thử thâm nhập bảo mật (Penetration testing) trên các API phụ trợ liên quan đến đơn hàng, cũng như không xây dựng ma trận chuyển đổi trạng thái (State Transition Matrix) đầy đủ cho đơn hàng.

### 2. Cách cải tiến prompt để tối ưu hóa AI
1. **Prompt yêu cầu kiểm tra tĩnh công thức toán học và logic so sánh.**
2. **Prompt định hướng kiểm thử an ninh (Security & Access Control) và phân quyền.**
3. **Prompt kiểm thử hộp xám (Grey-box testing) kết hợp giao diện và dữ liệu.**
4. **Prompt yêu cầu kiểm thử ma trận trạng thái (State Transition Matrix) cho các biến có trạng thái phức tạp.**


---
---

# FEATURE: FR-14 — QUẢN LÝ DANH MỤC (CATEGORY CRUD)

## 1. Domain Testing — FR-14

**SUT:** Giao diện Web Admin (`http://localhost:5174`) + API `POST/DELETE /api/categories` + Database bảng `categories`

### Bước 1 — Phạm vi và SUT

#### Tài liệu Đặc tả (SRS FR-14)
- Admin có quyền Thêm / Xem / Xóa danh mục.
- Tên danh mục là bắt buộc, không được phép để trống.
- Ngoài ra, đối chiếu theo **FR-12: Kiểm soát truy cập (Access Control)**, tất cả các API này phải yêu cầu xác thực JWT và người dùng có vai trò là admin (`role = 'admin'`).

#### Các file mã nguồn liên quan
- **Frontend Admin UI:** [App.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-admin/src/App.jsx) (dòng 103, 142-151, 153-160, 294-335)
- **Backend API:** [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) (dòng 243-278)
- **Database Schema:** [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js) (dòng 22-26 - bảng `categories`)

#### Phân tích sơ bộ từ mã nguồn thực tế (Code vs SRS)
1. **API categories thiếu phân quyền Admin:** `POST`, `PUT`, và `DELETE /api/categories` sử dụng middleware `authenticateToken` để kiểm tra đăng nhập nhưng **hoàn toàn bỏ quên** khâu kiểm tra vai trò admin (`req.user.role === 'admin'`). Điều này cho phép tài khoản người dùng thường thực thi được toàn bộ các thao tác CRUD danh mục.
2. **Thiếu validate tên danh mục ở Backend:** API `POST /api/categories` không kiểm tra giá trị `name` trước khi thực thi truy vấn SQLite `INSERT INTO categories`. Bảng `categories` cũng không cấu hình cột `name` là `NOT NULL`, do đó hệ thống cho phép tạo các danh mục có tên rỗng `""` hoặc `null`.
3. **Không xử lý lỗi xóa ID không tồn tại:** API `DELETE /api/categories/:id` không kiểm tra xem ID có tồn tại trước khi xóa hay không, và không kiểm tra `this.changes` sau khi chạy `DELETE`. Hệ thống luôn trả về `200 OK` ("Category deleted") đối với mọi ID rác gửi lên.
4. **Thiếu validate phía client trên Web Admin:** Form "Thêm mới" danh mục trên giao diện Admin không thực hiện kiểm tra `categoryName` rỗng trước khi gửi lên backend API.

### Bước 2 — Input Variables (Biến đầu vào)

| ID | Biến | Kiểu dữ liệu | Nguồn | Ràng buộc từ SRS |
|----|------|--------------|-------|------------------|
| V1 | `name` | String | Form UI / API Body | Bắt buộc nhập, không được để trống |
| V2 | `token` | String (JWT) | Headers | Token của tài khoản Admin (`role = 'admin'`) |
| V3 | `id` | Integer | URL Parameter | ID của danh mục, phải tồn tại khi xóa |

**Bộ giá trị hợp lệ mặc định (để kiểm thử đơn lỗi):**
- `name`: `"Sách"`
- `token`: `<Valid Admin Token>`
- `id`: `1` (Điện thoại - tồn tại mặc định)

### Bước 3 — Domains (Miền giá trị)

| Biến | Miền hợp lệ (Valid Domain) | Miền không hợp lệ (Invalid Domain) | Giá trị đặc biệt (Special/Edge Values) |
|------|----------------------------|-----------------------------------|---------------------------------------|
| **name** | Chuỗi chữ từ 1 ký tự trở lên | Chuỗi rỗng `""` | Khoảng trắng đầu/cuối, SQL Injection (`' OR 1=1--`), thẻ HTML/XSS |
| **token** | Token JWT hợp lệ của admin | Token JWT của user thường, token sai định dạng | Không truyền token (Guest) |
| **id** | ID nguyên dương đang tồn tại trong DB | ID không tồn tại trong DB | ID là số âm, bằng 0, ký tự không phải số |

### Bước 4 — Equivalence Partitions (Phân vùng tương đương)

| EP-ID | Loại vùng | Biến tác động | Mô tả phân vùng tương đương | Giá trị đại diện |
|-------|-----------|---------------|-----------------------------|------------------|
| **EP-N01** | Hợp lệ | `name` | Tên danh mục thông thường hợp lệ | `"Sách"` |
| **EP-N02** | Không hợp lệ | `name` | Tên danh mục bị bỏ trống | `""` |
| **EP-N03** | Không hợp lệ | `name` | Tên danh mục chỉ gồm khoảng trắng | `"   "` |
| **EP-A01** | Hợp lệ | `token` | Token hợp lệ của tài khoản Admin | `role = 'admin'` |
| **EP-A02** | Không hợp lệ | `token` | Token của tài khoản User thường | `role = 'user'` |
| **EP-A03** | Không hợp lệ | `token` | Khách vãng lai chưa đăng nhập | *Không gửi token* |
| **EP-I01** | Hợp lệ | `id` | ID tồn tại trong DB | `1` |
| **EP-I02** | Không hợp lệ | `id` | ID không tồn tại trong DB | `9999` |

### Bước 5 — Constraints (Các ràng buộc nghiệp vụ)

| C-ID | Ràng buộc nghiệp vụ / Hệ thống | Loại ràng buộc | Kết quả kỳ vọng |
|------|-------------------------------|----------------|-----------------|
| **C-01** | Quyền hạn thao tác | Ràng buộc chéo | Chỉ admin mới được Thêm/Xóa danh mục. Hệ thống từ chối các role khác. |
| **C-02** | Bắt buộc nhập tên | Ràng buộc định dạng | Validate dữ liệu ở cả Client và Server để từ chối tên rỗng. |
| **C-03** | Tham chiếu toàn vẹn | Ràng buộc DB | Ràng buộc xử lý lỗi khi xóa danh mục không tồn tại hoặc ID không hợp lệ. |

### Bước 6 — Test Cases thiết kế từ Domain Testing

| TC-ID | Mô tả kịch bản kiểm thử | Input thực tế đầu vào | Kết quả mong đợi theo SRS | Phân vùng EP / Ràng buộc |
|-------|-------------------------|-----------------------|---------------------------|-------------------------|
| **DT-01** | Admin thêm danh mục hợp lệ (Happy Path) | token=`Admin`, name=`"Sach"` | Thêm danh mục thành công, trả về HTTP 200/201 | EP-N01, EP-A01, C-02 |
| **DT-02** | Admin thêm danh mục với tên rỗng | token=`Admin`, name=`""` | Từ chối, báo lỗi tên bắt buộc (HTTP 400 Bad Request) | EP-N02, C-02 |
| **DT-03** | Admin thêm danh mục chỉ chứa khoảng trắng | token=`Admin`, name=`"   "` | Từ chối, báo lỗi tên không hợp lệ (HTTP 400 Bad Request) | EP-N03, C-02 |
| **DT-04** | User thường thêm danh mục (Access Bypass) | token=`User`, name=`"Normal User Category"` | Từ chối thao tác, báo lỗi phân quyền (HTTP 403 Forbidden) | EP-A02, C-01 |
| **DT-05** | Khách vãng lai thêm danh mục | token=`Không có`, name=`"Guest Category"` | Từ chối thao tác, báo lỗi xác thực (HTTP 401 Unauthorized) | EP-A03, C-01 |
| **DT-06** | Admin xóa danh mục đang tồn tại (Happy Path) | token=`Admin`, id=`<ID vừa tạo>` | Xóa danh mục thành công, trả về HTTP 200 OK | EP-I01, EP-A01, C-01 |
| **DT-07** | Admin xóa danh mục không tồn tại | token=`Admin`, id=`9999` | Báo lỗi không tìm thấy danh mục (HTTP 404 Not Found) | EP-I02, C-03 |
| **DT-08** | User thường xóa danh mục (Access Bypass) | token=`User`, id=`1` | Từ chối thao tác, báo lỗi phân quyền (HTTP 403 Forbidden) | EP-A02, C-01 |
| **DT-09** | Khách vãng lai xóa danh mục | token=`Không có`, id=`1` | Từ chối thao tác, báo lỗi xác thực (HTTP 401 Unauthorized) | EP-A03, C-01 |
| **DT-10** | SQL Injection trong trường Tên danh mục | name=`"Books' OR 1=1--"` | Lưu trữ an toàn tên dạng chuỗi, không lỗi DB | Giá trị đặc biệt |
| **DT-11** | XSS (Cross-Site Scripting) trong Tên danh mục | name=`"<script>alert('XSS')</script>"` | Lưu trữ an toàn, render escape tránh thực thi mã độc | Giá trị đặc biệt |

---

## 2. Boundary Value Analysis — FR-14

**SUT:** Giao diện Web Admin + API `POST/DELETE /api/categories`

### Bước 1 — Xác định các biên (Boundaries) từ đặc tả SRS

Dựa vào SRS FR-14, ta xác định các biên sau:

| B-ID | Biến | Ràng buộc SRS | Điểm biên dưới (Min) | Điểm biên trên (Max) | Kiểu biên |
|------|------|---------------|----------------------|----------------------|-----------|
| **B-NAME-LEN** | `name` | Độ dài tên danh mục | 1 ký tự | Không giới hạn | Giá trị số |
| **B-ID-VAL** | `id` | Giá trị ID danh mục để xóa | 1 | Không giới hạn | Giá trị số nguyên |

### Bước 2 — Xác định các điểm kiểm thử biên (BVA Points)

#### 1. Phân tích biên cho độ dài tên danh mục (B-NAME-LEN)
- **Sát dưới biên (Min - 1):** 0 ký tự (`name=""`). Kỳ vọng: **Từ chối (Reject)**
- **Tại biên (Min):** 1 ký tự (`name="A"`). Kỳ vọng: **Chấp nhận (Accept)**
- **Sát trên biên (Min + 1):** 2 ký tự (`name="AB"`). Kỳ vọng: **Chấp nhận (Accept)**

#### 2. Phân tích biên cho ID danh mục (B-ID-VAL)
- **Sát dưới biên (Min - 1):** `id = 0`. Kỳ vọng: **Từ chối (Reject / HTTP 404)**
- **Dưới biên nữa:** `id = -1`. Kỳ vọng: **Từ chối**
- **Tại biên (Min):** `id = 1`. Kỳ vọng: **Chấp nhận (Xóa nếu có quyền admin và tồn tại)**

### Bước 3 — Danh sách Test Cases thiết kế từ BVA

*Mặc định: Sử dụng token Admin hợp lệ.*

| TC-ID | Đầu vào kiểm thử | Vùng biên kiểm tra | Expected (SRS) | Expected (Backend thực tế) | Kết quả kỳ vọng |
|-------|------------------|-------------------|----------------|----------------------------|-----------------|
| **BV-01** | `name = ""` | Độ dài tên Min - 1 | Từ chối | Chấp nhận (do thiếu validate) | **FAIL** (Lỗi logic biên) |
| **BV-02** | `name = "A"` | Độ dài tên Min | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-03** | `name = "AB"` | Độ dài tên Min + 1 | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-04** | `id = 0` | ID biên dưới Min - 1 | Từ chối | Chấp nhận trả về `200` | **FAIL** (Lỗi logic biên) |
| **BV-05** | `id = -1` | ID âm | Từ chối | Chấp nhận trả về `200` | **FAIL** (Lỗi logic biên) |

---

## 3. Test Execution — FR-14

**Ngày thực thi:** 2026-06-10  
**Môi trường:** Windows 10, Node.js v22.20.0, SQLite, Chrome / Admin Web (:5174)

### Kết quả tổng hợp (Test Summary)

| Chỉ số (Metric) | Số lượng (Count) |
|-----------------|------------------|
| Tổng số kịch bản thiết kế | 16 |
| Đã thực thi (Executed) | 16 |
| **ĐẠT (Pass)** | 7 |
| **KHÔNG ĐẠT (Fail)** | 9 |
| Chưa chạy (Not run) | 0 |

### Nhật ký thực thi API Layer (`POST/DELETE /api/categories`)

Thực hiện kiểm thử gọi API trực tiếp thông qua script chạy tự động:

| TC-ID | Dữ liệu đầu vào (Request Body / URL) | HTTP Code | Kết quả thực tế (Actual Result) | Kết quả mong đợi (Expected) | Trạng thái | Mã lỗi (Bug ID) |
|-------|-----------------------------|-----------|---------------------------------|----------------------------|------------|-----------------|
| **DT-01** | POST name=`"Sach"`, Admin Token | 200 OK | `{"message":"Category created","id":4}` | Thêm thành công danh mục | **PASS** | — |
| **DT-02** | POST name=`""`, Admin Token | 200 OK | `{"message":"Category created","id":5}` | Từ chối, báo lỗi `400 Bad Request` | **FAIL** | [BUG-003](./Consolidated_Bug_Report.md#bug-003-api-post-apicategories-khong-validate-ten-danh-muc-bi-bo-trong-empty-name) |
| **DT-03** | POST name=`"   "`, Admin Token | 200 OK | `{"message":"Category created","id":6}` | Từ chối, báo lỗi `400 Bad Request` | **FAIL** | [BUG-004](./Consolidated_Bug_Report.md#bug-004-api-post-apicategories-cho-phep-tao-danh-muc-chi-chua-khoang-trang) |
| **DT-04** | POST name=`"Normal User Category"`, User Token | 200 OK | `{"message":"Category created","id":7}` | Từ chối, báo lỗi phân quyền `403` | **FAIL** | [BUG-001](./Consolidated_Bug_Report.md#bug-001-api-post-apicategories-thieu-kiem-soat-phan-quyen-broken-access-control) |
| **DT-05** | POST name=`"Guest Category"`, Không Token | 401 | `{"error":"Unauthorized"}` | Từ chối, báo lỗi xác thực `401` | **PASS** | — |
| **DT-06** | DELETE `/api/categories/8`, Admin Token | 200 OK | `{"message":"Category deleted"}` | Xóa thành công danh mục | **PASS** | — |
| **DT-07** | DELETE `/api/categories/9999`, Admin Token | 200 OK | `{"message":"Category deleted"}` | Báo lỗi không tìm thấy `404` | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-api-delete-apicategoriesid-phan-hoi-thanh-cong-khi-xoa-id-khong-ton-tai-hoac-khong-hop-le) |
| **DT-08** | DELETE `/api/categories/8`, User Token | 200 OK | `{"message":"Category deleted"}` | Từ chối, báo lỗi phân quyền `403` | **FAIL** | [BUG-002](./Consolidated_Bug_Report.md#bug-002-api-delete-apicategoriesid-thieu-kiem-soat-phan-quyen-broken-access-control) |
| **DT-09** | DELETE `/api/categories/8`, Không Token | 401 | `{"error":"Unauthorized"}` | Từ chối, báo lỗi xác thực `401` | **PASS** | — |
| **DT-10** | POST name=`"Books' OR 1=1--"`, Admin Token | 200 OK | `{"message":"Category created","id":9}` | Lưu trữ an toàn không lỗi SQL | **PASS** | — |
| **DT-11** | POST name=`"<script>alert('XSS')</script>"`, Admin Token | 200 OK | `{"message":"Category created","id":10}` | Lưu trữ an toàn chuỗi thô | **PASS** | — |
| **BV-01** | POST name=`""`, Admin Token | 200 OK | Tạo thành công ID 5 | Từ chối biên dưới | **FAIL** | [BUG-003](./Consolidated_Bug_Report.md#bug-003-api-post-apicategories-khong-validate-ten-danh-muc-bi-bo-trong-empty-name) |
| **BV-02** | POST name=`"A"`, Admin Token | 200 OK | Tạo thành công | Chấp nhận | **PASS** | — |
| **BV-04** | DELETE `/api/categories/0`, Admin Token | 200 OK | `{"message":"Category deleted"}` | Từ chối ID không hợp lệ | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-api-delete-apicategoriesid-phan-hoi-thanh-cong-khi-xoa-id-khong-ton-tai-hoac-khong-hop-le) |
| **BV-05** | DELETE `/api/categories/-1`, Admin Token | 200 OK | `{"message":"Category deleted"}` | Từ chối ID không hợp lệ | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-api-delete-apicategoriesid-phan-hoi-thanh-cong-khi-xoa-id-khong-ton-tai-hoac-khong-hop-le) |

### Nhật ký thực thi UI / Code Review (Web Admin)

| TC-ID | Nội dung kiểm thử | Kết quả thực tế (UI & Code) | Kết quả mong đợi (SRS) | Trạng thái | Mã lỗi (Bug ID) |
|-------|-------------------|-----------------------------|------------------------|------------|-----------------|
| **DT-02 (UI)** | Thêm danh mục rỗng trên giao diện | Form submit trực tiếp lên API, không có khâu validate client | Chặn submit, báo lỗi rỗng | **FAIL** | [BUG-006](./Consolidated_Bug_Report.md#bug-006-giao-dien-web-admin-cho-phep-them-moi-danh-muc-rong-client-side-validation-bypass) |

### Đánh giá & Khuyến nghị
- **Phân quyền (Broken Access Control):** Cần sửa middleware hoặc thêm middleware kiểm tra vai trò admin (kiểm tra `req.user && req.user.role === 'admin'`) trên các API: `POST /api/categories`, `PUT /api/categories/:id`, `DELETE /api/categories/:id`.
- **Ràng buộc nghiệp vụ (Business Rules):** Bổ sung khâu validate dữ liệu `name` không rỗng ở backend trước khi thực thi truy vấn cơ sở dữ liệu. Đồng thời, thêm kiểm tra `categoryName.trim()` ở client-side để hiển thị cảnh báo giao diện tốt hơn.
- **SQLite error handling:** Sửa API DELETE để kiểm tra xem bản ghi có bị ảnh hưởng hay không (bằng cách kiểm tra `this.changes === 0`) nhằm trả về lỗi `404 Not Found` khi xóa ID rác.

---

## 4. AI Gap Analysis — FR-14

### 1. Các lỗi thực tế AI (Antigravity) đã bỏ sót trong các lượt chạy trước (Factual AI Gaps)

- **Lỗi thực tế bỏ sót:** Lỗ hổng SQL Injection nghiêm trọng tại API tìm kiếm sản phẩm (`GET /api/products?search=`).
  - **Chi tiết:** Trong tệp [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) dòng 141-150, API tìm kiếm sản phẩm trực tiếp ghép chuỗi truy vấn đầu vào (`searchQuery`) vào câu truy vấn SQLite mà không tham số hóa hoặc lọc dữ liệu đầu vào (`const query = "SELECT * FROM products WHERE name LIKE '%" + searchQuery + "%'"`;). Lỗ hổng này cho phép kẻ tấn công thực thi các câu lệnh SQL tùy ý để trích xuất toàn bộ dữ liệu nhạy cảm (như bảng `users` chứa plaintext mật khẩu của tất cả mọi người).
  - **Nguyên nhân bỏ sót thực tế:** Tính năng tìm kiếm sản phẩm không phải là đối tượng kiểm thử chính được định nghĩa trong luồng CRUD Danh mục (FR-14) của SRS, nên AI đã bỏ qua việc rà soát bảo mật đối với các API liên quan kề cận trong cùng tệp mã nguồn backend.

### 2. Cách cải tiến prompt để tối ưu hóa AI
1. **Prompt yêu cầu kiểm thử bảo mật phân quyền chéo (Role-based access check).**
2. **Prompt phân tích biên Robustness và lỗi ngầm định của SQLite.**
3. **Prompt đối chiếu tĩnh mã nguồn frontend và backend API.**
4. **Prompt kiểm thử thâm nhập an ninh (Security Penetration Testing) như SQL Injection và XSS cho toàn bộ codebase.**


---
---

# FEATURE: FR-02 (MOBILE) — ĐĂNG NHẬP & KHÓA TÀI KHOẢN

## 1. Domain Testing — FR-02 (Mobile)

**SUT:** Giao diện Đăng nhập trên Mobile App (`App.js`) + API backend `/api/login` + Database cột `login_attempts` và `locked_until` của bảng `users`

### Bước 1 — Phạm vi và SUT

#### Tài liệu Đặc tả (SRS FR-02)
- Người dùng nhập Email và Mật khẩu để đăng nhập.
- Bộ đếm đăng nhập sai tăng đúng 1 đơn vị sau mỗi lần thất bại.
- Đăng nhập sai liên tiếp từ 3 lần trở lên sẽ tạm khóa tài khoản trong 30 giây (môi trường demo).
- Hệ thống trả về thông báo lỗi phù hợp khi bị khóa, không tiết lộ lý do cụ thể để bảo mật.
- Đăng nhập thành công trả về JWT Token và gửi kèm qua header `Authorization: Bearer <token>` cho các API sau đó.

#### Các file mã nguồn liên quan
- **Frontend Mobile:** [App.js](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-mobile/App.js) (dòng 37-41, 186-207, 759-795)
- **Backend API:** [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) (dòng 32-66)
- **Database Schema:** [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js) (dòng 48-61 - bảng `users`)

#### Phân tích sơ bộ từ mã nguồn thực tế (Code vs SRS)
1. **Nhãn giao diện di động bị sai:** Nhãn hiển thị của ô nhập Email được đặt tên là `"Username"` thay vì `"Email"`.
2. **Thiếu tối ưu bàn phím di động:** Ô nhập Email không cấu hình `keyboardType="email-address"`, gây bất tiện cho người dùng khi nhập trên điện thoại.
3. **Che giấu lỗi khóa tài khoản ở Client:** Catch block của hàm `handleLogin` luôn ghi đè và ẩn tất cả các thông báo lỗi lỗi của server (bao gồm thông báo khóa tài khoản `403`) và chỉ hiển thị chuỗi tĩnh: `"Đăng nhập thất bại. Vui lòng kiểm tra lại."`.
4. **Backend tăng attempts sai đơn vị:** Mỗi lần đăng nhập sai, backend thực hiện `user.login_attempts + 2` (tăng 2 đơn vị thay vì 1), dẫn đến việc người dùng bị khóa tài khoản chỉ sau 2 lần nhập sai liên tiếp.
5. **Backend cấu hình sai thời gian khóa:** Backend khóa tài khoản trong 3 phút (180 giây) thay vì 30 giây theo SRS.

### Bước 2 — Input Variables (Biến đầu vào)

| ID | Biến | Kiểu dữ liệu | Nguồn | Ràng buộc từ SRS |
|----|------|--------------|-------|------------------|
| V1 | `email` | String | TextInput UI / API Body | Phải nhập đúng định dạng email |
| V2 | `password` | String | TextInput UI / API Body | Mật khẩu tài khoản |
| V3 | `login_attempts` | Integer | Database | Bộ đếm tăng 1 đơn vị mỗi lần nhập sai |
| V4 | `locked_until` | Datetime | Database | Thời gian khóa (30 giây sau khi bị khóa) |

**Bộ giá trị hợp lệ mặc định:**
- `email`: `"test@eshop.com"`
- `password`: `"Test1234!"`

### Bước 3 — Domains (Miền giá trị)

| Biến | Miền hợp lệ (Valid Domain) | Miền không hợp lệ (Invalid Domain) | Giá trị đặc biệt (Special/Edge Values) |
|------|----------------------------|-----------------------------------|---------------------------------------|
| **email** | Email đã đăng ký trong DB | Email chưa đăng ký, sai định dạng | Chuỗi rỗng `""`, ký tự đặc biệt |
| **password** | Khớp với password lưu trong DB | Không khớp với password trong DB | Chuỗi rỗng `""` |
| **login_attempts** | Số lần đăng nhập sai < 3 | Số lần đăng nhập sai >= 3 (bị khóa) | Bằng 0, số âm |
| **locked_until** | Giá trị thời gian đã qua (hoặc NULL) | Giá trị thời gian lớn hơn thời điểm hiện tại | Giá trị rác |

### Bước 4 — Equivalence Partitions (Phân vùng tương đương)

| EP-ID | Loại vùng | Biến tác động | Mô tả phân vùng tương đương | Giá trị đại diện |
|-------|-----------|---------------|-----------------------------|------------------|
| **EP-E01** | Hợp lệ | `email` | Email đã đăng ký trong hệ thống | `"test@eshop.com"` |
| **EP-E02** | Không hợp lệ | `email` | Email chưa đăng ký trong hệ thống | `"unknown@eshop.com"` |
| **EP-E03** | Không hợp lệ | `email` | Để trống email | `""` |
| **EP-P01** | Hợp lệ | `password` | Nhập đúng mật khẩu của tài khoản | `"Test1234!"` |
| **EP-P02** | Không hợp lệ | `password` | Nhập sai mật khẩu | `"wrong_pass"` |
| **EP-P03** | Không hợp lệ | `password` | Để trống mật khẩu | `""` |
| **EP-L01** | Hợp lệ | `login_attempts` | Số lần đăng nhập sai chưa vượt ngưỡng | `0`, `1`, `2` |
| **EP-L02** | Không hợp lệ | `login_attempts` | Số lần đăng nhập sai vượt ngưỡng khóa | `>= 3` |

### Bước 5 — Constraints (Các ràng buộc nghiệp vụ)

| C-ID | Ràng buộc nghiệp vụ / Hệ thống | Loại ràng buộc | Kết quả kỳ vọng |
|------|-------------------------------|----------------|-----------------|
| **C-01** | Khóa tài khoản liên tiếp | Ràng buộc chéo | Đăng nhập sai >= 3 lần liên tiếp thì tài khoản bị khóa trong 30 giây. |
| **C-02** | Reset bộ đếm khi thành công | Logic nghiệp vụ | Đăng nhập thành công phải reset `login_attempts = 0` và `locked_until = NULL`. |
| **C-03** | Bảo mật thông tin lỗi | Ràng buộc UI | Không thông báo chi tiết lỗi là sai email hay sai mật khẩu, nhưng cần báo nếu tài khoản đang bị khóa. |

### Bước 6 — Test Cases thiết kế từ Domain Testing

| TC-ID | Mô tả kịch bản kiểm thử | Input thực tế đầu vào | Kết quả mong đợi theo SRS | Phân vùng EP / Ràng buộc |
|-------|-------------------------|-----------------------|---------------------------|-------------------------|
| **DT-01** | Đăng nhập thành công (Happy Path) | email=`"test@eshop.com"`, password=`"Test1234!"` | Đăng nhập thành công, chuyển hướng về Home | EP-E01, EP-P01, C-02 |
| **DT-02** | Đăng nhập với Email chưa đăng ký | email=`"unknown@eshop.com"`, password=`"wrong"` | Từ chối, báo lỗi sai email hoặc mật khẩu | EP-E02 |
| **DT-03** | Đăng nhập với Email rỗng | email=`""`, password=`"Test1234!"` | Báo lỗi hoặc chặn yêu cầu gửi đi | EP-E03 |
| **DT-04** | Đăng nhập với Mật khẩu rỗng | email=`"test@eshop.com"`, password=`""` | Báo lỗi hoặc chặn yêu cầu gửi đi | EP-P03 |
| **DT-05** | Kiểm tra nhãn trường nhập Email trên di động | Đọc trực quan màn hình đăng nhập di động | Trường nhập Email hiển thị nhãn là "Email" | UI review |
| **DT-06** | Kiểm tra tối ưu bàn phím di động cho trường Email | Click vào ô nhập Email | Bàn phím ảo di động hiển thị nút `@` nhanh | UI review |
| **DT-07** | Đăng nhập thành công đính kèm header xác thực | Đăng nhập thành công và thực hiện xem đơn hàng | Request lấy đơn hàng có header `Authorization: Bearer <Token>` | C-02 |
| **DT-08** | Hiển thị thông báo khi tài khoản bị khóa | Đăng nhập bằng mật khẩu đúng khi tài khoản đang bị khóa | Hiển thị thông báo tài khoản bị khóa trên giao diện di động | EP-L02, C-03 |

---

## 2. Boundary Value Analysis — FR-02 (Mobile)

**SUT:** Giao diện đăng nhập di động + API backend `/api/login` + DB

### Bước 1 — Xác định các biên (Boundaries) từ đặc tả SRS

| B-ID | Biến | Ràng buộc SRS | Điểm biên dưới (Min) | Điểm biên trên (Max) | Kiểu biên |
|------|------|---------------|----------------------|----------------------|-----------|
| **B-LIMIT-CNT** | `login_attempts` | Ngưỡng khóa tài khoản | 3 lần | Không giới hạn | Số lần đếm |
| **B-LOCK-DUR** | `lock_duration` | Thời gian khóa | 30 giây | 30 giây | Giá trị thời gian |

### Bước 2 — Xác định các điểm kiểm thử biên (BVA Points)

#### 1. Phân tích biên cho số lần đăng nhập sai liên tiếp (B-LIMIT-CNT)
- **Sát dưới biên (Min - 1):** Đăng nhập sai 2 lần -> Kỳ vọng: **Tài khoản chưa khóa**
- **Tại biên (Min):** Đăng nhập sai 3 lần -> Kỳ vọng: **Tài khoản bắt đầu khóa**
- **Sát trên biên (Min + 1):** Đăng nhập sai 4 lần -> Kỳ vọng: **Tài khoản vẫn khóa**

#### 2. Phân tích biên cho thời gian khóa tài khoản (B-LOCK-DUR)
- **Sát dưới biên (Min - 1s):** Đợi 29 giây -> Kỳ vọng: **Tài khoản vẫn đang khóa**
- **Tại biên (Min):** Đợi 30 giây -> Kỳ vọng: **Tài khoản tự động mở khóa**
- **Sát trên biên (Min + 1s):** Đợi 31 giây -> Kỳ vọng: **Tài khoản đã mở khóa**

### Bước 3 — Danh sách Test Cases thiết kế từ BVA

| TC-ID | Đầu vào kiểm thử | Vùng biên kiểm tra | Expected (SRS) | Expected (Backend thực tế) | Kết quả kỳ vọng |
|-------|------------------|-------------------|----------------|----------------------------|-----------------|
| **BV-01** | Nhập sai mật khẩu 1 lần | Số lần sai = 1 | Không khóa | Không khóa (attempts = 2) | Chấp nhận |
| **BV-02** | Nhập sai mật khẩu 2 lần | Số lần sai = 2 | Không khóa | Bị khóa tài khoản (attempts = 4) | **FAIL** (Khóa quá sớm) |
| **BV-03** | Nhập sai mật khẩu 3 lần | Số lần sai = 3 | Khóa tài khoản | Bị khóa tài khoản | Chấp nhận |
| **BV-04** | Đợi 30 giây sau khi bị khóa | Thời gian khóa Min | Tài khoản mở khóa | Tài khoản vẫn khóa (do khóa 180s) | **FAIL** (Khóa quá lâu) |
| **BV-05** | Đợi 29 giây sau khi bị khóa | Thời gian khóa Min - 1 | Tài khoản vẫn khóa | Tài khoản vẫn khóa | Chấp nhận |

---

## 3. Test Execution — FR-02 (Mobile)

**Ngày thực thi:** 2026-06-10  
**Môi trường:** Windows 10, Node.js v22.20.0, SQLite, React Native Expo App (SUT)

### Kết quả tổng hợp (Test Summary)

| Chỉ số (Metric) | Số lượng (Count) |
|-----------------|------------------|
| Tổng số kịch bản thiết kế | 13 |
| Đã thực thi (Executed) | 13 |
| **ĐẠT (Pass)** | 5 |
| **KHÔNG ĐẠT (Fail)** | 8 |
| Chưa chạy (Not run) | 0 |

### Nhật ký thực thi API Layer (`POST /api/login`)

Thực hiện kiểm thử gọi trực tiếp API login ở backend:

| TC-ID | Dữ liệu đầu vào (Request Body) | HTTP Code | Kết quả thực tế (Actual Result) | Kết quả mong đợi (Expected) | Trạng thái | Mã lỗi (Bug ID) |
|-------|-----------------------------|-----------|---------------------------------|----------------------------|------------|-----------------|
| **DT-01** | `email="test@eshop.com"`, `password="Test1234!"` | 200 OK | Đăng nhập thành công, trả về token và user | Đăng nhập thành công | **PASS** | — |
| **DT-02** | `email="unknown@eshop.com"`, `password="wrong"` | 401 | `{"error":"Invalid email or password"}` | Từ chối đăng nhập | **PASS** | — |
| **BV-01** | `password="wrong"` (Lần 1) | 401 | `attempts = 2` | attempts tăng lên 1 | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-bo-dem-so-lan-dang-nhap-sai-tang-sai-don-vi-tang-2-thay-vi-tang-1) |
| **BV-02** | `password="wrong"` (Lần 2) | 401 | `attempts = 4`, `locked_until` được đặt 180s | Tài khoản chưa bị khóa | **FAIL** | [BUG-005](./Consolidated_Bug_Report.md#bug-005-bo-dem-so-lan-dang-nhap-sai-tang-sai-don-vi-tang-2-thay-vi-tang-1) |
| **DT-08** | `password="Test1234!"` (Đăng nhập khi đang khóa) | 403 | `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` | Từ chối đăng nhập, trả về mã lỗi 403 | **PASS** | — |
| **BV-04** | Chờ 30 giây và thử lại | 403 | Vẫn bị lỗi khóa tài khoản 403 | Đăng nhập thành công (mở khóa sau 30s) | **FAIL** | [BUG-004](./Consolidated_Bug_Report.md#bug-004-api-backend-cau-hinh-sai-thoi-gian-khoa-tai-khoan-180-giay-thay-vi-30-giay) |

### Nhật ký thực thi UI / Code Review (Mobile App)

| TC-ID | Nội dung kiểm thử | Kết quả thực tế (UI & Code) | Kết quả mong đợi (SRS) | Trạng thái | Mã lỗi (Bug ID) |
|-------|-------------------|-----------------------------|------------------------|------------|-----------------|
| **DT-05** | Nhãn trường nhập Email trên giao diện | Nhãn hiển thị là `"Username"` (Dòng 763 file `App.js`) | Nhãn phải là `"Email"` | **FAIL** | [BUG-001](./Consolidated_Bug_Report.md#bug-001-nhan-hien-thi-truong-nhap-email-dang-nhap-bi-sai-thanh-username) |
| **DT-06** | Ô nhập Email thiếu thuộc tính tối ưu | Thẻ TextInput không có thuộc tính `keyboardType` (Dòng 764-770) | TextInput có thuộc tính `keyboardType="email-address"` | **FAIL** | [BUG-002](./Consolidated_Bug_Report.md#bug-002-o-nhap-email-khong-cau-hinh-thuoc-tinh-keyboardtype%3Demail-address) |
| **DT-08** | Giao diện di động ẩn lỗi khóa tài khoản | Catch block ghi đè toàn bộ lỗi và chỉ hiện thông báo tĩnh: `"Đăng nhập thất bại. Vui lòng kiểm tra lại."` (Dòng 204-206) | Hiển thị thông báo lỗi khóa từ backend để người dùng biết | **FAIL** | [BUG-003](./Consolidated_Bug_Report.md#bug-003-ung-dung-di-dong-ghi-de-va-an-thong-bao-khoa-tai-khoan-tu-server) |
| **DT-07** | Đăng nhập thành công gửi kèm token | Headers được đính kèm: `{ Authorization: "Bearer <token>" }` | Headers đính kèm token hợp lệ | **PASS** | — |

### Đánh giá & Khuyến nghị
- **Mobile UI:** Cập nhật lại nhãn hiển thị từ `Username` thành `Email`, thêm thuộc tính `keyboardType="email-address"` vào TextInput của email.
- **Mobile Logic:** Thay đổi catch block trong hàm `handleLogin` để hiển thị lỗi thực tế từ server trả về (`error.message`) thay vì ghi đè bằng một câu thông báo chung chung.
- **Backend API:** Sửa logic cộng dồn attempts ở tệp `server.js` thành `user.login_attempts + 1` và đổi thời gian tạm khóa tài khoản thành 30 giây (`30000` ms) thay vì 3 phút để phù hợp với môi trường demo SRS.

---

## 4. AI Gap Analysis — FR-02 (Mobile)

### 1. Các lỗi thực tế AI (Antigravity) đã bỏ sót trong các lượt chạy trước (Factual AI Gaps)

- **Lỗi thực tế bỏ sót 1:** Biểu thức chính quy kiểm tra số điện thoại bị sai tại hàm cập nhật hồ sơ di động (`handleUpdateProfile`).
  - **Chi tiết:** Trong tệp [App.js](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-mobile/App.js) dòng 287, biểu thức chính quy `!/^[1-9][0-9]{8,9}$/.test(phone)` chặn tất cả các số điện thoại bắt đầu bằng chữ số `0` (vốn là định dạng chuẩn bắt buộc của số điện thoại Việt Nam). Điều này ép buộc người dùng di động phải nhập số điện thoại không có số 0 ở đầu.
- **Lỗi thực tế bỏ sót 2:** Thiếu kiểm tra và xác thực dữ liệu đầu vào phía Client tại Form Đăng nhập di động (Login Form Validation Bypass).
  - **Chi tiết:** Trong tệp [App.js](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-mobile/App.js) dòng 186-207, hàm `handleLogin` không hề kiểm tra xem các trường Email và Password có bị bỏ trống hay không trước khi gửi yêu cầu mạng POST trực tiếp lên API backend, gây lãng phí tài nguyên mạng.
- **Lỗi thực tế bỏ sót 3:** Thiếu cơ chế lưu trữ bền vững Token đăng nhập (Missing Session Token Persistence).
  - **Chi tiết:** Token đăng nhập chỉ được lưu trữ trong React State (`const [token, setToken] = useState("");`), hoàn toàn không sử dụng thư viện lưu trữ bền vững như `AsyncStorage`. Điều này khiến người dùng bị đăng xuất ngay lập tức khi ứng dụng di động reload hoặc khởi chạy lại.
- **Nguyên nhân bỏ sót thực tế:** AI chỉ tập trung chạy kịch bản tự động hóa API đăng nhập và xem qua giao diện Login/Lockout cơ bản theo yêu cầu tối thiểu, mà không kiểm tra thực tế luồng tương tác sau đăng nhập (như cập nhật hồ sơ) hoặc kiểm tra tính bền vững của phiên đăng nhập (Session Persistence).

### 2. Cách cải tiến prompt để tối ưu hóa AI
1. **Prompt yêu cầu rà soát cấu trúc xử lý lỗi và hiển thị thông báo lỗi ở client.**
2. **Prompt kiểm tra tối ưu hóa giao diện di động (Platform UX attributes).**
3. **Prompt yêu cầu truy vấn trực tiếp cơ sở dữ liệu để kiểm tra trạng thái bộ đếm.**
4. **Prompt yêu cầu kiểm thử tính bền vững của phiên làm việc (Session/Token Persistence) và kiểm thử định dạng đặc thù quốc gia (Local format validation).**



