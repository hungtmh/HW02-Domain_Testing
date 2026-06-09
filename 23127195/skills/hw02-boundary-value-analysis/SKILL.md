---
name: hw02-boundary-value-analysis
description: >-
  Applies Boundary Value Analysis (BVA) to design test cases for EShop features.
  Use when the user asks for boundary value analysis, BVA, boundary testing, or
  edge case test design for numeric, length, or count constraints on EShop.
---

# Boundary Value Analysis — EShop

## Nguyên tắc

BVA tập trung vào **biên** của miền đầu vào: min, max, just below min, just above max, và giá trị điển hình trong miền.

Áp dụng **sau** Domain Testing — dùng các partition đã xác định, trích boundary từ ràng buộc SRS.

## Quy trình 5 bước (ghi trong báo cáo)

### Bước 1 — Trích xuất boundary từ SRS

Đọc FR trong `README.md`, liệt kê mọi ràng buộc có ngưỡng:

| Biến | Ràng buộc SRS | Min | Max | Kiểu biên |
|------|---------------|-----|-----|-----------|
| password | ≥ 8 ký tự | 8 | ∞ | length |
| phone | 0 + 10-11 số | 10 digits | 11 digits | length |
| login_fail | khóa từ 3 lần | 3 | — | count |
| quantity | int ≥ 1 | 1 | stock? | numeric |
| price | > 0 | 0 (invalid) | — | numeric |
| min_order_amount | ≥ threshold | boundary value | — | numeric |

### Bước 2 — Xác định điểm test cho mỗi biên

Với biên **đóng** (closed): test `min`, `min-1`, `min+1`, `max`, `max-1`, `max+1`

Ví dụ password length 8:
- BV-01: 7 ký tự (invalid, just below)
- BV-02: 8 ký tự (valid, on boundary)
- BV-03: 9 ký tự (valid, just above)

### Bước 3 — Robust BVA (nếu cần)

Thêm: empty, null, whitespace-only, overflow (rất lớn), negative

### Bước 4 — Multi-variable BVA

**Single-fault assumption**: khi test biên của biến A, giữ biến khác ở giá trị hợp lệ trung tâm.

Chỉ kết hợp nhiều biên khi có **ràng buộc chéo** rõ (ví dụ FR-09: total vs min_order_amount)

### Bước 5 — Sinh test case

```markdown
| TC-ID | Biến | Giá trị | Loại biên | Kết quả mong đợi |
| BV-01 | password length | 7 | min-1 | Từ chối — chưa đủ 8 ký tự |
| BV-02 | password length | 8 | min (valid) | Chấp nhận nếu đủ hoa/thường/số/đặc biệt |
```

## Boundary cheat sheet — EShop SRS

| Feature | Boundary cụ thể |
|---------|-----------------|
| FR-01 password | 7 vs 8 chars; thiếu hoa/thường/số/special |
| FR-02 lockout | sai 2 lần (chưa khóa) vs 3 lần (khóa 30s) vs đúng sau khóa |
| FR-03 OTP | 5 vs 6 vs 7 chữ số |
| FR-04 phone | 9 số, 10 số, 11 số, 12 số; không bắt đầu bằng 0 |
| FR-06 quantity | 0, 1, 2; số âm; chữ |
| FR-09 coupon | total = min-1, min, min+1; EXPIRED date |
| FR-15 price | 0, 0.01, -1 |
| FR-16 CSV | dòng đầu header; price=0 một dòng → rollback all |
| FR-17 max_uses_per_user | 0, 1; min_order_amount -1 vs 0 |

## Template output

Lưu `23127195/reports/FR-XX_bva.md`:

```markdown
# Boundary Value Analysis — FR-XX: [Tên]

## 1. Boundaries identified
| B-ID | Biến | Min | Max | Nguồn SRS |
...

## 2. BVA points
| Point | Value | Relation to boundary |
...

## 3. Test Cases
| TC-ID | Input | Boundary tested | Expected (SRS) | Actual | Pass/Fail |
| BV-01 | ... | min-1 | ... | | |
```

## Thực thi

1. Chạy từng BV test trên SUT
2. Ghi **Actual** — khác Expected → bug report
3. Đặc biệt chú ý off-by-one (lockout 2 vs 3, phone 10 vs 11)

## Sau khi thiết kế

- So sánh với Domain Testing — tránh trùng TC không cần thiết, nhưng BV phải cover đủ biên
- AI gap analysis: AI hay bỏ sót biên `min-1` hoặc concurrent boundary
- Commit: `test(FR-XX): design and execute BVA test cases`

## Tham chiếu

- `23127195/templates/bva-template.md`
- Skill `hw02-domain-testing` — partitions đã có
