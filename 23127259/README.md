# Nguyễn Tấn Thắng Nhóm 08 mssv 23127259 - HW02 Domain Testing & Boundary Value Analysis

## 1. Thông tin sinh viên

- **Họ và tên:** Nguyễn Tấn Thắng
- **Nhóm:** Nhóm 08
- **MSSV:** 23127259
- **Môn học:** Kiểm thử phần mềm (Software Testing)
- **Bài tập:** HW02 - Domain Testing & Boundary Value Analysis (BVA)

---

## 2. Bảng tự đánh giá kết quả (Self-Assessment)

| STT | Tiêu chí | Điểm tối đa | Điểm tự đánh giá | Minh chứng |
|-----|----------|-------------|------------------|------------|
| 1 | **Feature A** (FR-02: Login and account lockout) | 25 | **25** | Domain + BVA, 15 TC, 2 bug trong [Main_Report.md](./reports/Main_Report.md) |
| 2 | **Feature B** (FR-07: Shopping cart) | 25 | **25** | Domain + BVA, 18 TC, 5 bug trong [Main_Report.md](./reports/Main_Report.md) |
| 3 | **Feature C** (FR-16: Product import from CSV) | 25 | **25** | Domain + BVA, 15 TC, 3 bug trong [Main_Report.md](./reports/Main_Report.md) |
| 4 | **Feature D Mobile** (Mobile Product listing/search) | 15 | **15** | Domain + BVA, 16 TC, 4 bug trong [Main_Report.md](./reports/Main_Report.md) |
| 5 | **Agent Skills** | 10 | **10** | Bộ skill trong [skills/](./skills/) |
| | **TỔNG ĐIỂM** | **100** | **100** | **Đạt yêu cầu điểm tối đa** |

---

## 3. Danh sách tính năng lựa chọn kiểm thử (Features Selected)

| Pool | Feature ID | Tên chức năng | Thành phần SUT | URL kiểm thử thực tế |
|------|------------|---------------|----------------|----------------------|
| **Pool A** | **FR-02** | Login and account lockout | Web Client & API Backend | `http://localhost:5173/login`, `POST /api/login` |
| **Pool B** | **FR-07** | Shopping cart | Web Client | `http://localhost:5173/cart` |
| **Pool C** | **FR-16** | Product import from CSV | Web Admin & API Backend | `POST /api/admin/import-products` |
| **Pool D** | **Mobile Product listing/search** | Danh sách và tìm kiếm sản phẩm mobile | React Native Expo Mobile | Mobile home screen |

---

## 4. Tóm tắt kết quả kiểm thử (Test Summary Report)

| Chỉ số kiểm thử (Test Metric) | Số lượng (Count) | Ghi chú |
|-------------------------------|------------------|---------|
| **Tổng số chức năng đã kiểm thử** | **4** | FR-02, FR-07, FR-16, Mobile Product listing/search |
| **Tổng số Test Case đã thiết kế** | **64** | Domain Testing & BVA |
| **Tổng số Test Case đã thực thi/review** | **33** | API evidence + source review |
| **Số Test Case ĐẠT (Passed)** | **10** | Đúng đặc tả hoặc source review pass |
| **Số Test Case KHÔNG ĐẠT (Failed)** | **23** | Sai khác so với SRS |
| **Số Test Case chưa thực thi** | **31** | Chưa chạy UI/device trực tiếp |
| **Tổng số lỗi phát hiện (Bugs Found)** | **14** | 2 FR-02, 5 FR-07, 3 FR-16, 4 Mobile |

---

## 5. Video Demo (Demo Videos & Agent Skills)

- **Link YouTube Demo:** TBD

Các skill của Agent được tổ chức giống thư mục mẫu:
1. `hw02-workflow`
2. `hw02-domain-testing`
3. `hw02-boundary-value-analysis`
4. `hw02-bug-report`
5. `hw02-ai-audit-report`
6. `hw02-eshop-setup`

---

## 6. Cấu trúc thư mục báo cáo

- **[Main_Report.md](./reports/Main_Report.md):** Báo cáo kiểm thử chính.
- **[Bug_Report.md](./reports/Bug_Report.md):** Báo cáo lỗi hợp nhất.
- **[AI_Critique.md](./reports/AI_Critique.md):** Nhận xét quá trình sử dụng AI.
- **[AI_Audit_Report.md](./reports/AI_Audit_Report.md):** Nhật ký tương tác AI.
- **[git_commit_log.txt](./reports/git_commit_log.txt):** Lịch sử commit Git.
- **[FR-02_bugs/](./reports/FR-02_bugs/)**, **[FR-07_bugs/](./reports/FR-07_bugs/)**, **[FR-16_bugs/](./reports/FR-16_bugs/)**, **[Mobile-product-listing_bugs/](./reports/Mobile-product-listing_bugs/)**: ảnh minh chứng bug.

---

## 7. Liên kết Repository & Đóng góp

- **GitHub Issues:** [hungtmh/HW02-Domain_Testing/issues](https://github.com/hungtmh/HW02-Domain_Testing/issues)
- Issue link trong báo cáo đang để TBD để cập nhật sau khi tạo issue thật.
