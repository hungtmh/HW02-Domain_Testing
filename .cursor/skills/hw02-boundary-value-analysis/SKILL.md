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

### Bước 2 — Xác định điểm test cho mỗi biên

Với biên **đóng** (closed): test `min`, `min-1`, `min+1`, `max`, `max-1`, `max+1`

### Bước 3 — Robust BVA (nếu cần)

Thêm: empty, null, whitespace-only, overflow (rất lớn), negative

### Bước 4 — Multi-variable BVA

**Single-fault assumption**: khi test biên của biến A, giữ biến khác ở giá trị hợp lệ trung tâm.

### Bước 5 — Sinh test case

## Vị trí lưu trữ dữ liệu

Ghi nhận thông tin vào file báo cáo chính: **`23127195/reports/Main_Testing_Report.md`** tại mục:
`# FEATURE: FR-XX — [Tên]` -> `## 2. Boundary Value Analysis — FR-XX`

### Cấu trúc Markdown ghi nhận:

```markdown
## 2. Boundary Value Analysis — FR-XX: [Tên feature]

### Bước 1 — Xác định các biên (Boundaries) từ đặc tả SRS
| B-ID | Biến | Ràng buộc SRS | Điểm biên dưới (Min) | Điểm biên trên (Max) | Kiểu biên |
...

### Bước 2 — Xác định các điểm kiểm thử biên (BVA Points)
...

### Bước 3 — Danh sách Test Cases thiết kế từ BVA
| TC-ID | Input | Vùng biên kiểm tra | Expected (SRS) | Expected (UI thực tế) | Expected (API thực tế) |
| BV-01 | ... | ... | ... | | |
...

### Bước 4 — Kịch bản biên Robustness / Edge cases bổ sung
| TC-ID | Đầu vào kiểm thử | Mục đích kiểm tra | Kết quả mong đợi |
...
```

## Thực thi

1. Chạy từng BV test trên SUT
2. Ghi **Actual** và cập nhật bảng chạy test của SUT dưới mục `## 3. Test Execution — FR-XX` của file `Main_Testing_Report.md`.
3. Đặc biệt chú ý off-by-one (lockout 2 vs 3, phone 10 vs 11).

## Sau khi thiết kế

- So sánh với Domain Testing — tránh trùng TC không cần thiết, nhưng BV phải cover đủ biên
- Commit: `test(FR-XX): design and execute BVA test cases`
