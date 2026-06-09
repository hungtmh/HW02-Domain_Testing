# Boundary Value Analysis — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**Ngày:** 2026-06-08  
**SUT:** Frontend Web + `POST /api/register`

---

## Bước 1 — Boundaries từ SRS

| B-ID | Biến | Ràng buộc SRS | Min (valid) | Max | Kiểu |
|------|------|---------------|-------------|-----|------|
| B-PW-LEN | password | Độ dài ≥ 8 | 8 ký tự | không giới hạn SRS | length |
| B-PW-UPPER | password | ≥ 1 chữ hoa | 1 | — | composition |
| B-PW-LOWER | password | ≥ 1 chữ thường | 1 | — | composition |
| B-PW-DIGIT | password | ≥ 1 số | 1 | — | composition |
| B-PW-SPEC | password | ≥ 1 trong `@$!%*?&` | 1 | — | composition |
| B-NAME | name | Không rỗng | 1 ký tự | — | length |

---

## Bước 2 — BVA Points

### Password length (B-PW-LEN)

| Point | Giá trị | Quan hệ biên |
|-------|---------|--------------|
| P-L1 | `Test1!` (7 ký tự, đủ loại) | min − 1 → reject |
| P-L2 | `Test12!` (8 ký tự) | min → accept nếu đủ composition |
| P-L3 | `Test123!` (9 ký tự) | min + 1 → accept |

### Composition — thiếu từng thành phần (giữ length ≥ 8)

| Point | Password | Thiếu |
|-------|----------|-------|
| P-C1 | `test1234!` | uppercase |
| P-C2 | `TEST1234!` | lowercase |
| P-C3 | `TestTest!` | digit |
| P-C4 | `Test1234` | special char |

### Implementation-specific boundary (từ code Web)

Regex thực tế yêu cầu **khoảng trắng** `\s` thay vì special SRS:

| Point | Password | Ý nghĩa |
|-------|----------|---------|
| P-IMPL1 | `Test1234!` | Hợp lệ SRS, **không** có space → Web reject? |
| P-IMPL2 | `Test 1234` | Có space, không special SRS → Web accept? |

---

## Bước 3 — Test Cases

*Các biến khác giữ giá trị hợp lệ: `name="Nguyen Van A"`, `email=<unique mỗi TC>`*

| TC-ID | Input (password) | Boundary | Expected (SRS) | Actual (đã chạy) | Pass/Fail |
|-------|------------------|----------|----------------|------------------|-----------|
| BV-01 | `Test12!` (7 chars) | len min−1 | Reject | API: **200 OK** đăng ký thành công | **FAIL** |
| BV-02 | `Test123!` (8 chars) | len min | Accept | API: 200 OK | PASS (API) |
| BV-03 | `Test1234!` (9 chars) | len min+1 | Accept | API: 200 OK | PASS (API) |
| BV-04 | `test1234!` | thiếu hoa | Reject | API: 200 OK | **FAIL** |
| BV-05 | `TEST1234!` | thiếu thường | Reject | API: 200 OK | **FAIL** |
| BV-06 | `TestTest!` | thiếu số | Reject | API: 200 OK | **FAIL** |
| BV-07 | `Test1234` | thiếu special | Reject | API: 200 OK | **FAIL** |
| BV-08 | `Test1234!` | SRS valid, no space | Accept (Web) | Web regex: **reject** (báo yếu) | **FAIL** |
| BV-09 | `Test 1234` | có space, no SRS special | Reject (SRS) | Web: **accept** nếu submit | **FAIL** |
| BV-10 | name = ` ` (1 space) | name min | Reject | Chưa chạy UI | Not run |
| BV-11 | email `a@b.co` | email ngắn hợp lệ | Accept | API: 200 (nếu unique) | PASS (API) |
| BV-12 | duplicate `test@eshop.com` | uniqueness | Reject | API: **200 OK** id mới | **FAIL** |

---

## Bước 4 — Robust / Edge

| TC-ID | Input | Ghi chú | Expected |
|-------|-------|---------|----------|
| BV-R01 | password rỗng | HTML5 required | Không submit |
| BV-R02 | email `user@domain` (no TLD) | format edge | Reject |
| BV-R03 | password 256+ ký tự | overflow | Reject hoặc accept có giới hạn |
| BV-R04 | Unicode name `Nguyễn Văn A` | i18n | Accept |

---

## Tóm tắt

| Metric | Số lượng |
|--------|----------|
| Boundary identified | 6 nhóm |
| BVA test cases | 16 |
| Executed (API) | 8 |
| Fail | 6 |
| Not run (UI) | 8 |
