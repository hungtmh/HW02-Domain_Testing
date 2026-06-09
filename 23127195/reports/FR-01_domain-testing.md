# Domain Testing — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**Ngày:** 2026-06-09  
**SUT:** Frontend Web (`http://localhost:5173/register`) + API `POST /api/register`

---

## Bước 1 — Phạm vi và SUT

### Tài liệu Đặc tả (SRS FR-01)
- **Các trường thông tin bắt buộc:** Họ Tên, Email, Mật khẩu, Xác nhận mật khẩu.
- **Ràng buộc định dạng Email:** Phải có định dạng hợp lệ (`user@domain.com`) và là **duy nhất** trong hệ thống.
- **Ràng buộc Mật khẩu mạnh:** Tối thiểu 8 ký tự, chứa ít nhất: 1 chữ cái in hoa, 1 chữ cái in thường, 1 chữ số, và 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`).
- **Trường Xác nhận mật khẩu:** Hệ thống phải kiểm tra xem giá trị nhập vào có khớp với trường Mật khẩu hay không. Nếu không khớp, từ chối đăng ký.
- **Hành vi sau khi thành công:** Người dùng được chuyển hướng tới trang Đăng nhập (`/login`).

### Các file mã nguồn liên quan
- **Frontend Web:** [Register.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Register.jsx)
- **Routing:** [App.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/App.jsx)
- **Backend API:** [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) (dòng 20–30)
- **Database:** [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js) (dòng 50-61 - bảng `users`)

### Phân tích sơ bộ từ mã nguồn thực tế (Code vs SRS)
1. **Thiếu trường dữ liệu:** Form đăng ký trên giao diện Frontend Web hoàn toàn **không có trường Xác nhận mật khẩu** (`confirmPassword`).
2. **Regex mật khẩu bị sai:** Regex kiểm tra mật khẩu mạnh ở Frontend (`flawedStrongPasswordRegex` tại dòng 15 của `Register.jsx`) yêu cầu **khoảng trắng** (`\s`) thay vì ký tự đặc biệt theo SRS, và loại trừ tất cả các ký tự đặc biệt chuẩn (`@`, `$`, `!`, v.v.).
3. **Backend bỏ qua xác thực:** API `POST /api/register` trên backend không thực hiện bất kỳ khâu kiểm tra định dạng hoặc độ mạnh mật khẩu nào.
4. **Trùng lặp email:** Bảng `users` trong cơ sở dữ liệu SQLite không định nghĩa cột `email` là `UNIQUE`, đồng thời backend không kiểm tra email đã tồn tại trước khi ghi nhận bản ghi mới.

---

## Bước 2 — Input Variables

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

---

## Bước 3 — Domains (Miền giá trị)

| Biến | Miền hợp lệ (Valid Domain) | Miền không hợp lệ (Invalid Domain) | Giá trị đặc biệt (Special/Edge Values) |
|------|----------------------------|-----------------------------------|---------------------------------------|
| **name** | Chuỗi chữ từ 1 ký tự trở lên | Chuỗi rỗng `""` | Khoảng trắng đầu/cuối, thẻ HTML/XSS (`<script>`), SQL Injection (`' OR 1=1--`) |
| **email** | Đúng định dạng email RFC, chưa tồn tại trong DB | Sai định dạng, đã tồn tại trong DB | Chứa ký tự Unicode, TLD cực ngắn hoặc cực dài, giá trị rỗng |
| **password** | Độ dài >= 8, chứa ít nhất 1 hoa, 1 thường, 1 số, 1 ký tự đặc biệt SRS | Độ dài < 8, thiếu một trong các thành phần bắt buộc | Chứa khoảng trắng, SQL Injection, chuỗi siêu dài |
| **confirmPassword** | Khớp 100% với `password` | Khác biệt so với `password` | Để trống khi `password` đã nhập |

---

## Bước 4 — Equivalence Partitions (Phân vùng tương đương)

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

---

## Bước 5 — Constraints (Các ràng buộc nghiệp vụ)

| C-ID | Ràng buộc nghiệp vụ | Loại ràng buộc | Hành vi kỳ vọng của hệ thống |
|------|---------------------|----------------|------------------------------|
| **C-01** | Khớp mật khẩu | Ràng buộc chéo | `confirmPassword` phải giống hệt `password` thì mới kích hoạt submit. |
| **C-02** | Email duy nhất | Ràng buộc nghiệp vụ | Hệ thống từ chối đăng ký và trả lỗi nếu `email_in_db == true`. |
| **C-03** | Mật khẩu mạnh | Ràng buộc định dạng | Validate mật khẩu dựa trên cấu trúc SRS ở cả Client và Server. |
| **C-04** | Sau thành công | Luồng hậu điều kiện | Thực hiện lưu trữ thông tin và chuyển hướng (redirect) về `/login`. |
| **C-05** | Trường bắt buộc | Ràng buộc giao diện | Các ô nhập bắt buộc phải được đánh dấu và ngăn chặn submit rỗng ở Client. |

---

## Bước 6 — Test Cases thiết kế từ Domain Testing

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

## Tóm tắt Coverage của Domain Testing

- **Tổng số phân vùng EP:** 18 phân vùng.
- **Tổng số Test Cases thiết kế:** 13 test cases.
- **Phạm vi phủ sóng:** Phủ kín tất cả các trường dữ liệu đầu vào và các ràng buộc nghiệp vụ của SRS.
