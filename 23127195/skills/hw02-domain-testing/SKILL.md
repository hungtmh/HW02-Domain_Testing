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

### Bước 3 — Xác định miền (Domains) cho từng biến

Phân loại:
- **Valid domain** — giá trị hợp lệ
- **Invalid domain** — giá trị không hợp lệ
- **Special values** — rỗng, null, SQL/XSS string, Unicode, khoảng trắng đầu/cuối

### Bước 4 — Equivalence Partitioning

Chia mỗi biến thành các **lớp tương đương** (EP).

### Bước 5 — Ràng buộc chéo (Constraints)

- **Independence**: biến độc lập → test từng biến, giữ biến khác ở giá trị hợp lệ mặc định
- **Dependencies**: mật khẩu khớp xác nhận; coupon cần total >= min_order_amount

### Bước 6 — Chọn test case (Coverage strategy)

Ưu tiên:
1. Mỗi EP ít nhất 1 TC
2. Mỗi constraint ít nhất 1 TC vi phạm + 1 TC thỏa
3. Luồng end-to-end (happy path + alternate path)

## Vị trí lưu trữ dữ liệu

Ghi nhận thông tin vào file báo cáo chính: **`23127195/reports/Main_Testing_Report.md`** tại mục:
`# FEATURE: FR-XX — [Tên]` -> `## 1. Domain Testing — FR-XX`

### Cấu trúc Markdown ghi nhận:

```markdown
## 1. Domain Testing — FR-XX: [Tên feature]

### Bước 1 — Phạm vi và SUT
...

### Bước 2 — Input variables
| ID | Biến | Miền hợp lệ | Miền không hợp lệ |
...

### Bước 3 — Equivalence Partitions
| EP-ID | Mô tả | Biến | Đại diện |
...

### Bước 4 — Constraints
...

### Bước 5 — Test Cases
| TC-ID | Mô tả | Input | Kết quả mong đợi (theo SRS) | EP/Constraint |
| DT-01 | ... | ... | ... | EP-01 |
```

## Sau khi thiết kế

1. Đối chiếu code thực tế — implementation có thể khác SRS (đó là bug)
2. Ghi AI gap analysis nếu AI bỏ sót partition
3. Commit: `test(FR-XX): design domain test cases`
