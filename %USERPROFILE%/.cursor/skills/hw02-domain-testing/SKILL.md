---
name: hw02-domain-testing
description: >-
  Applies Domain Testing technique to design test cases for EShop features.
  Use when the user asks for domain testing, equivalence partitioning, input
  domain analysis, or test case design for FR-01 through FR-20 on EShop.
---

# Domain Testing — EShop

## Nguyên tắc

Domain Testing = xác định **miền đầu vào** → **phân vùng** → **chọn test case** phủ các vùng và ràng buộc chéo.

**KHÔNG** chỉ liệt kê test case. Phải giải thích từng bước áp dụng kỹ thuật.

## Quy trình 6 bước (bắt buộc ghi trong báo cáo)

### Bước 1 — Xác định SUT và phạm vi

- Đọc mục FR tương ứng trong `README.md`
- Xác định: Web / Admin / Mobile / API
- Liệt kê file code liên quan (ví dụ `frontend-web/src/pages/Login.jsx`, `backend/server.js`)

### Bước 2 — Liệt kê biến đầu vào (Input Variables)

Với mỗi biến ghi:

| Biến | Kiểu | Nguồn (UI/API) | Ràng buộc từ SRS |
|------|------|----------------|------------------|

Ví dụ FR-01 Register: `name`, `email`, `password`, `confirmPassword`

### Bước 3 — Xác định miền (Domains) cho từng biến

Phân loại:

- **Valid domain** — giá trị hợp lệ
- **Invalid domain** — giá trị không hợp lệ
- **Special values** — rỗng, null, SQL/XSS string, Unicode, khoảng trắng đầu/cuối

### Bước 4 — Equivalence Partitioning

Chia mỗi biến thành các **lớp tương đương** (EP):

```
EP-01: email hợp lệ, chưa tồn tại
EP-02: email hợp lệ, đã tồn tại
EP-03: email sai định dạng
EP-04: email rỗng
...
```

### Bước 5 — Ràng buộc chéo (Constraints)

- **Independence**: biến độc lập → test từng biến, giữ biến khác ở giá trị hợp lệ mặc định
- **Dependencies**: `password` phải khớp `confirmPassword`; coupon cần `total >= min_order_amount`
- Ghi constraint dạng: `IF email valid AND password weak THEN reject`

### Bước 6 — Chọn test case (Coverage strategy)

Ưu tiên:

1. Mỗi EP ít nhất 1 TC
2. Mỗi constraint ít nhất 1 TC vi phạm + 1 TC thỏa
3. Luồng end-to-end (happy path + alternate path)
4. Bổ sung case phát hiện bug thực tế sau khi đọc code

## Template test case

Lưu vào `23127195/reports/FR-XX_domain-testing.md`:

```markdown
# Domain Testing — FR-XX: [Tên feature]

## 1. Phạm vi và SUT
...

## 2. Input variables
| ID | Biến | Miền hợp lệ | Miền không hợp lệ |
...

## 3. Equivalence Partitions
| EP-ID | Mô tả | Biến | Đại diện |
...

## 4. Constraints
...

## 5. Test Cases
| TC-ID | Mô tả | Input | Kết quả mong đợi (theo SRS) | EP/Constraint |
| DT-01 | ... | ... | ... | EP-01 |
```

## Mapping FR → input thường gặp

| FR | Biến chính cần phân vùng |
|----|--------------------------|
| FR-01 | name, email, password, confirmPassword |
| FR-02 | email, password, failed_attempts, lockout_duration |
| FR-03 | email, otp, newPassword, confirmPassword, step |
| FR-04 | name, phone (0 + 10-11 số), shippingAddress |
| FR-05 | search keyword (empty, normal, XSS, no result) |
| FR-06 | productId, quantity (int ≥ 1) |
| FR-07 | cart items, quantity, delete confirm |
| FR-08 | auth token, cart state, total_amount (server-side) |
| FR-09 | coupon code, total, user_id, expiry, min_amount, max_uses |
| FR-10 | order status transitions, actor (user/admin) |
| FR-14-19 | CRUD fields theo SRS admin |

## Sau khi thiết kế

1. Đối chiếu code thực tế — implementation có thể khác SRS (đó là bug)
2. Ghi AI gap analysis nếu AI bỏ sót partition
3. Commit: `test(FR-XX): design domain test cases`

## Tham chiếu

- SRS: `README.md`
- Template: `23127195/templates/domain-testing-template.md`
