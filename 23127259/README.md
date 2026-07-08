# Nguyễn Tấn Thắng Nhóm 08 mssv 23127259 - HW02 Domain Testing & Boundary Value Analysis

## 1. Thông tin sinh viên

- **Họ và tên:** Nguyễn Tấn Thắng
- **Nhóm:** Nhóm 08
- **MSSV:** 23127259
- **Môn học:** Kiểm thử phần mềm
- **Bài tập:** HW02 - Domain Testing & Boundary Value Analysis
- **Ngày chạy test/evidence:** 2026-07-05 20:13 ICT
- **Ngày đồng bộ báo cáo cuối:** 2026-07-06

---

## 1.1 Metadata gói nộp

| Trường | Giá trị |
|--------|---------|
| Folder bài nộp trong repo nhóm | `/Users/thangnhi/Downloads/HW02-Domain_Testing/23127259` |
| Format | Theo cấu trúc repo nhóm, tương tự thư mục mẫu `23127195` |
| Nguồn đồng bộ nội dung | `/Users/thangnhi/Documents/23127259_HW02_AI_DomainTesting_100` |
| Evidence | Lưu trong `reports/*_bugs/` theo từng feature |
| Markdown/PDF | `README.md`, `Main_Report.md`, `Bug_Report.md`, `AI_Audit_Report.md`, `AI_Critique.md` đều có PDF tương ứng |
| Video evidence | 1 video cho FR-07 BUG-003: `reports/FR-07_bugs/BUG-003.mov` |
| Agent skills demo video | [https://youtu.be/ePMQMkoJTsM](https://youtu.be/ePMQMkoJTsM) |

---

## 2. Bảng tự đánh giá kết quả

| STT | Tiêu chí | Điểm tối đa | Điểm tự đánh giá | Minh chứng |
|-----|----------|-------------|------------------|------------|
| 1 | Feature A - FR-02 Login and account lockout | 25 | 25 | Domain Testing, BVA, API test và source review trong [Main_Report.md](./reports/Main_Report.md) |
| 2 | Feature B - FR-07 Shopping cart | 25 | 25 | API test cart, UI evidence và video BUG-FR07-003 trong [Main_Report.md](./reports/Main_Report.md) |
| 3 | Feature C - FR-16 Product import from CSV | 25 | 25 | API test import, access control, rollback và CSV parser review trong [Main_Report.md](./reports/Main_Report.md) |
| 4 | Feature D - Mobile Product listing/search | 15 | 15 | API search test + source review mobile app trong [Main_Report.md](./reports/Main_Report.md) |
| 5 | Agent Skills / AI Usage Evidence | 10 | 10 | Có [AI_Audit_Report.md](./reports/AI_Audit_Report.md), [AI_Critique.md](./reports/AI_Critique.md), [agent-skills/demo-video-link.md](./agent-skills/demo-video-link.md), `skills/`, `templates/` |
| | **Tổng điểm** | **100** | **100** | Hoàn thành đủ cấu trúc nộp bài |

---

## 3. Danh sách tính năng lựa chọn

| Pool | Feature ID | Tên chức năng | Thành phần SUT | Cách kiểm thử |
|------|------------|---------------|----------------|---------------|
| Pool A | FR-02 | Login and account lockout | Web Client + API Backend | `POST /api/login`, source `Login.jsx`, DB state |
| Pool B | FR-07 | Shopping cart | Web Client + API Backend | `GET/POST /api/cart`, source `CartContext.jsx`, `Cart.jsx` |
| Pool C | FR-16 | Product import from CSV | Web Admin + API Backend | `POST /api/admin/import-products`, source `App.jsx` admin |
| Pool D | Mobile Product listing/search | Danh sách và tìm kiếm sản phẩm trên Mobile | React Native Expo + API Backend | `GET /api/products`, source `frontend-mobile/App.js` |

---

## 4. Tóm tắt kết quả kiểm thử

Test thực tế được chạy trên SUT tại `/Users/thangnhi/Downloads/eshop-sut`, backend đang phục vụ ở `http://localhost:3000`.

| Chỉ số kiểm thử | Số lượng | Ghi chú |
|-----------------|----------|---------|
| Tổng số chức năng kiểm thử | 4 | FR-02, FR-07, FR-16, Mobile listing/search |
| Tổng số test case đã thiết kế | 48 | Gồm Domain Testing và BVA |
| Test case đã thực thi/review | 28 | API execution + static source review |
| Test case pass | 10 | Kết quả khớp SRS |
| Test case fail | 18 | Có sai khác so với SRS |
| Test case chưa chạy trực tiếp | 20 | Chủ yếu là UI/device boundary chưa mở thiết bị thật |
| Tổng số bug có evidence | 16 | FR-02: 3, FR-07: 5, FR-16: 4, Mobile: 4 |
| Demo video | 1 | Agent skills demo: [https://youtu.be/ePMQMkoJTsM](https://youtu.be/ePMQMkoJTsM); FR-07 BUG-003: thao tác xóa giỏ hàng không có confirm dialog |

### Kết quả theo feature

| Feature | Designed | Executed/Reviewed | Pass | Fail | Not run | Bugs |
|---------|----------|-------------------|------|------|---------|------|
| FR-02 Login and account lockout | 12 | 7 | 2 | 5 | 5 | 3 |
| FR-07 Shopping cart | 12 | 7 | 2 | 5 | 5 | 5 |
| FR-16 Product import from CSV | 12 | 7 | 3 | 4 | 5 | 4 |
| Mobile Product listing/search | 12 | 7 | 3 | 4 | 5 | 4 |
| **Tổng** | **48** | **28** | **10** | **18** | **20** | **16** |

---

## 5. Ghi chú chạy test thực tế

- **Thời điểm chạy:** 2026-07-05 20:13 ICT.
- **Base URL:** `http://localhost:3000/api`.
- **Test data prefix:** `live_hw02_1783257224503`.
- **Cleanup:** đã kiểm tra lại DB, không còn user/product test có prefix `live_hw02_%`.
- **Evidence screenshots/video:** ảnh `.png`, `.jpg` và video `.mov` trong các thư mục bug là minh chứng từ quá trình thao tác UI/API trực tiếp trên EShop SUT. Riêng `FR-07 BUG-003` dùng video để thể hiện thao tác xóa sản phẩm không có confirm dialog.
- **Lint check:** `npm run lint` trên `frontend-web` và `frontend-admin` đều fail do lỗi code sẵn có; chi tiết được ghi trong [Main_Report.md](./reports/Main_Report.md).

---

## 6. Cấu trúc thư mục báo cáo

Toàn bộ tài liệu được tổ chức theo format repo nhóm giống thư mục mẫu `23127195`:

- [reports/Main_Report.md](./reports/Main_Report.md) / [Main_Report.pdf](./reports/Main_Report.pdf): Báo cáo kiểm thử chính, gồm Domain Testing, Boundary Value Analysis, test execution summary và tổng kết bug.
- [reports/Bug_Report.md](./reports/Bug_Report.md) / [Bug_Report.pdf](./reports/Bug_Report.pdf): 16 bug report có expected, actual, severity, priority, related test case và evidence.
- [reports/AI_Critique.md](./reports/AI_Critique.md) / [AI_Critique.pdf](./reports/AI_Critique.pdf): Nhận xét về việc dùng AI.
- [reports/AI_Audit_Report.md](./reports/AI_Audit_Report.md) / [AI_Audit_Report.pdf](./reports/AI_Audit_Report.pdf): Nhật ký tương tác AI.
- [reports/git_commit_log.txt](./reports/git_commit_log.txt): Commit log tham chiếu của SUT và ghi chú workspace.
- [reports/23127259_HW02_Combined_Report.pdf](./reports/23127259_HW02_Combined_Report.pdf): File PDF tổng hợp các báo cáo chính.
- [reports/FR-02_bugs/](./reports/FR-02_bugs/): Evidence cho FR-02.
- [reports/FR-07_bugs/](./reports/FR-07_bugs/): Evidence cho FR-07, có `BUG-003.mov` và `BUG-003-preview.png`.
- [reports/FR-16_bugs/](./reports/FR-16_bugs/): Evidence cho FR-16.
- [reports/Mobile-product-listing_bugs/](./reports/Mobile-product-listing_bugs/): Evidence cho Mobile listing/search.
- [agent-skills/demo-video-link.md](./agent-skills/demo-video-link.md) / [demo-video-link.pdf](./agent-skills/demo-video-link.pdf): Link YouTube demo agent skills.
- [skills/](./skills/): Bộ skill hỗ trợ workflow HW02.
- [templates/](./templates/): Template Domain Testing, BVA và README.

---

## 7. Repository / Issues

- **SUT local:** `/Users/thangnhi/Downloads/eshop-sut`
- **Folder bài nộp:** `/Users/thangnhi/Downloads/HW02-Domain_Testing/23127259`
- **GitHub repo nhóm:** https://github.com/hungtmh/HW02-Domain_Testing
- **GitHub Issues:** GitHub Issues đã tạo cho 16 bug: [#27](https://github.com/hungtmh/HW02-Domain_Testing/issues/27) đến [#42](https://github.com/hungtmh/HW02-Domain_Testing/issues/42). Danh sách chi tiết nằm trong [reports/Bug_Report.md](./reports/Bug_Report.md).
