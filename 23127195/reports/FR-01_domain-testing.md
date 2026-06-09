# Domain Testing — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**Ngày:** 2026-06-08  
**SUT:** Frontend Web (`http://localhost:5173/register`) + API `POST /api/register`

---

## Bước 1 — Phạm vi và SUT

### SRS (FR-01)

- Input: **Họ Tên**, **Email**, **Mật khẩu**, **Xác nhận mật khẩu**
- Email: định dạng hợp lệ, **duy nhất**
- Mật khẩu mạnh: ≥ 8 ký tự, 1 hoa, 1 thường, 1 số, 1 ký tự đặc biệt (`@$!%*?&`)
- Xác nhận mật khẩu phải khớp
- Thành công → chuyển trang Đăng nhập

### Files liên quan

| Layer | File |
|-------|------|
| Frontend Web | `frontend-web/src/pages/Register.jsx` |
| Routing | `frontend-web/src/App.jsx` |
| Backend API | `backend/server.js` (L20–30) |
| Database | `backend/database.js` (bảng `users`, **không** UNIQUE trên `email`) |

### Phát hiện sơ bộ từ code (ảnh hưởng domain)

- Web **không có** trường `confirmPassword`
- Web validate mật khẩu bằng regex **sai** (yêu cầu khoảng trắng thay vì ký tự đặc biệt)
- Backend **không validate** email/mật khẩu, lưu plaintext
- DB cho phép email trùng

---

## Bước 2 — Input Variables

| ID | Biến | Kiểu | Nguồn | Ràng buộc SRS |
|----|------|------|-------|---------------|
| V1 | name | string | Form | Bắt buộc, không rỗng |
| V2 | email | string | Form | Định dạng email hợp lệ, unique |
| V3 | password | string | Form | ≥8, hoa+thường+số+special |
| V4 | confirmPassword | string | Form | Khớp password |
| V5 | (implicit) | — | API | Email chưa tồn tại trong DB |

**Giá trị mặc định hợp lệ** (single-fault): `name="Nguyen Van A"`, `email=<unique>`, `password=confirmPassword="Test1234!"`

---

## Bước 3 — Domains

| Biến | Valid Domain | Invalid Domain | Special |
|------|--------------|----------------|---------|
| name | Chuỗi không rỗng | Rỗng, chỉ khoảng trắng | XSS `<script>`, SQL `' OR 1=1--` |
| email | `user@domain.com`, chưa tồn tại | Sai format, đã tồn tại | Unicode, uppercase domain |
| password | Đủ 4 loại ký tự + ≥8 | Thiếu hoa/thường/số/special, <8 | Chỉ space làm “special” |
| confirmPassword | = password | ≠ password | Rỗng khi password có giá trị |

---

## Bước 4 — Equivalence Partitions

| EP-ID | Mô tả | Biến | Giá trị đại diện |
|-------|-------|------|------------------|
| EP-N01 | Tên hợp lệ | name | `Nguyen Van A` |
| EP-N02 | Tên rỗng | name | `` (HTML5 `required` chặn submit) |
| EP-N03 | Tên chỉ whitespace | name | `   ` |
| EP-E01 | Email hợp lệ, mới | email | `user001@test.com` |
| EP-E02 | Email hợp lệ, đã tồn tại | email | `test@eshop.com` |
| EP-E03 | Email sai định dạng | email | `not-an-email` |
| EP-E04 | Email rỗng | email | `` |
| EP-P01 | Mật khẩu hợp lệ theo SRS | password | `Test1234!` |
| EP-P02 | Mật khẩu < 8 ký tự | password | `Test1!` |
| EP-P03 | Thiếu chữ hoa | password | `test1234!` |
| EP-P04 | Thiếu chữ thường | password | `TEST1234!` |
| EP-P05 | Thiếu số | password | `TestTest!` |
| EP-P06 | Thiếu ký tự đặc biệt (SRS) | password | `Test1234` |
| EP-P07 | Có khoảng trắng, không có special SRS | password | `Test 1234` |
| EP-C01 | Confirm khớp password | confirmPassword | `Test1234!` |
| EP-C02 | Confirm không khớp | confirmPassword | `Test1234@` |
| EP-C03 | Không có trường confirm (UI) | confirmPassword | *(missing)* |
| EP-F01 | Happy path đầy đủ | all | Tất cả hợp lệ |
| EP-F02 | Đăng ký xong → login | flow | navigate `/login` |

---

## Bước 5 — Constraints

| C-ID | Ràng buộc | Loại |
|------|-----------|------|
| C-01 | `confirmPassword === password` | Dependency (SRS) |
| C-02 | `email` unique trong hệ thống | Business rule |
| C-03 | `password` thỏa regex mạnh SRS | Validation |
| C-04 | `email` format RFC-like | Validation |
| C-05 | Sau success → redirect login | Post-condition |
| C-06 | FR-22: email `type="email"` | GUI |
| C-07 | FR-22: trường bắt buộc có `*` | GUI |
| C-08 | FR-21: nút submit màu xanh | GUI |

---

## Bước 6 — Test Cases

| TC-ID | Mô tả | Input | Expected (SRS) | EP/C |
|-------|-------|-------|----------------|------|
| DT-01 | Happy path — đăng ký thành công | name, email mới, pass+confirm hợp lệ | 201/200, redirect `/login` | EP-F01 |
| DT-02 | Email đã tồn tại | `test@eshop.com` | Từ chối, thông báo email trùng | EP-E02, C-02 |
| DT-03 | Email sai format | `invalid-email` | Từ chối | EP-E03, C-04 |
| DT-04 | Tên rỗng | name="" | Từ chối (client hoặc server) | EP-N02 |
| DT-05 | Mật khẩu yếu — thiếu special | `Test1234` | Từ chối | EP-P06, C-03 |
| DT-06 | Confirm không khớp | pass ≠ confirm | Từ chối | EP-C02, C-01 |
| DT-07 | Mật khẩu hợp lệ SRS nhưng không có space | `Test1234!` | Chấp nhận | EP-P01 |
| DT-08 | Mật khẩu có space, không special SRS | `Test 1234` | Từ chối theo SRS | EP-P07 |
| DT-09 | Thiếu trường xác nhận mật khẩu trên UI | chỉ 3 field | Phải có field confirm | EP-C03 |
| DT-10 | Email field type | inspect input | `type="email"` | C-06 |
| DT-11 | Nút Đăng ký màu | inspect UI | Nút xanh dương | C-08 |
| DT-12 | SQL injection trong email | `' OR '1'='1` | Từ chối / escape an toàn | Special |
| DT-13 | XSS trong name | `<script>alert(1)</script>` | Không execute khi hiển thị | Special |

---

## Tóm tắt coverage

- **Số EP:** 18  
- **Số TC Domain:** 13  
- **EP chưa cover trực tiếp:** EP-N03 (whitespace name) — có thể gộp vào BVA/robust
