# AI Gap Analysis — FR-01

**MSSV:** 23127195  
**Ngày:** 2026-06-08

---

## Test cases AI ban đầu hay bỏ sót

| TC | Mô tả | Lý do AI miss |
|----|-------|---------------|
| DT-07 / BV-08 | Mật khẩu `Test1234!` hợp lệ SRS nhưng Web reject | AI thường assume regex khớp SRS; cần **đọc code** `Register.jsx` |
| DT-09 | Thiếu hoàn toàn trường confirmPassword | AI chỉ đọc SRS, không đối chiếu UI thực tế |
| BV-12 | Email duplicate qua API | AI giả định DB có UNIQUE; schema thực tế không có |
| DT-11 | Màu nút submit đỏ thay vì xanh | AI tập trung functional test, bỏ qua FR-21 GUI |
| DT-10 | `type="text"` cho email | Cần inspect HTML, không chỉ test API |

---

## Bugs AI không phát hiện nếu chỉ prompt chung

| Bug | Lý do |
|-----|-------|
| BUG-001 Email trùng | Prompt "test register" không yêu cầu đọc `database.js` schema |
| BUG-003 name rỗng qua API | Client có `required` nhưng API không validate — cần test **cả 2 layer** |
| BUG-004 Backend không validate password length | Chỉ test UI sẽ miss API bypass |
| Plaintext password (SEC-01) | Cần đọc `server.js` INSERT trực tiếp |

---

## Cải thiện prompt lần sau

1. *"Đọc FR-01 trong README.md, sau đó đọc Register.jsx và POST /api/register trong server.js, liệt kê mọi khác biệt implementation vs SRS"*
2. *"Thiết kế domain partitions cho cả UI layer và API layer riêng"*
3. *"BVA password: test đúng 7, 8, 9 ký tự và từng loại thiếu hoa/thường/số/special"*
4. *"Kiểm tra FR-21, FR-22 GUI requirements trên form đăng ký"*

---

## Human review đã bổ sung

- Thêm TC kiểm tra regex implementation vs SRS (P-IMPL1, P-IMPL2)
- Thêm API-level tests bypass frontend validation
- Gộp bug SEC-01 (plaintext) vào phạm vi security reference
