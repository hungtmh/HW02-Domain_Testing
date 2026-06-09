# Test Execution — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**Ngày thực thi:** 2026-06-08  
**Môi trường:** Windows, Backend :3000, Frontend Web :5173  
**Người thực hiện:** 23127195 (+ AI assist, đã review)

---

## Kết quả tổng hợp

| Metric | Count |
|--------|-------|
| TC thiết kế (Domain + BVA, unique) | 24 |
| Đã thực thi | 12 |
| Pass | 4 |
| Fail | 8 |
| Not run | 12 |

---

## API Execution Log (`POST /api/register`)

| TC-ID | Request summary | Status | Actual | Expected | Result | Bug |
|-------|-----------------|--------|--------|----------|--------|-----|
| DT-01 | email=newuser001@test.com, pass=Test1234! | 200 | Registered id=3 | Success | PASS | — |
| DT-02 | email=test@eshop.com (duplicate) | 200 | Registered id=4,10 | Reject duplicate | **FAIL** | BUG-001 |
| DT-03 | email=invalid-email | 200 | Registered id=5 | Reject format | **FAIL** | BUG-002 |
| DT-04 | name="" | 200 | Registered id=6 | Reject | **FAIL** | BUG-003 |
| BV-01 | password 7 chars Test12! | 200 | Registered id=7 | Reject | **FAIL** | BUG-004 |
| BV-02 | password 8 chars Test123! | 200 | Registered id=8 | Accept | PASS | — |
| BV-03 | password 9 chars Test1234! | 200 | Registered id=9 | Accept | PASS | — |
| BV-07 | password Test1234 (no special) | — | (gộp DT-05) | Reject | **FAIL** | BUG-004 |

---

## UI / Code Review (chưa chạy browser, review source)

| TC-ID | Kiểm tra | Actual (code) | Expected (SRS) | Result | Bug |
|-------|----------|---------------|----------------|--------|-----|
| DT-06 | confirmPassword field | **Không có** field | Có field + validate khớp | **FAIL** | BUG-005 |
| DT-08 | pass `Test 1234` | Regex chấp nhận space | Reject (cần special SRS) | **FAIL** | BUG-006 |
| DT-07 | pass `Test1234!` | Regex **reject** (cần space) | Accept | **FAIL** | BUG-006 |
| DT-09 | 3 fields only | name, email, password | 4 fields | **FAIL** | BUG-005 |
| DT-10 | email input type | `type="text"` | `type="email"` | **FAIL** | BUG-007 |
| DT-11 | submit button color | `bg-red-500` | Blue primary | **FAIL** | BUG-008 |
| DT-01 flow | redirect after success | `navigate('/login')` | Redirect login | PASS | — |

---

## Ghi chú thực thi

- API tests chạy bằng PowerShell `Invoke-WebRequest` khi backend đang chạy.
- Backend không có lớp validation → hầu hết invalid input vẫn 200.
- UI tests cần chạy thủ công trên browser + chụp screenshot cho GitHub Issues.

---

## Next steps

1. Chạy UI tests DT-06, DT-07, DT-08, DT-10, DT-11 trên `:5173/register`
2. Tạo GitHub Issues cho BUG-001 → BUG-008
3. Chụp screenshot mỗi bug
