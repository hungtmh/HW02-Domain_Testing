# MSSV 23127195 — HW02 Domain Testing & Boundary Value Analysis

## 1. Thông tin sinh viên
- **Họ và tên:** Trần Mạnh Hùng (Nhóm 08)
- **MSSV:** 23127195
- **Môn học:** Kiểm thử phần mềm (Software Testing)
- **Bài tập:** HW02 — Domain Testing & Boundary Value Analysis (BVA)

---

## 2. Bảng tự đánh giá kết quả (Self-Assessment)

| STT | Tiêu chí | Điểm tối đa | Điểm tự đánh giá | Minh chứng |
|-----|----------|-------------|------------------|------------|
| 1   | **Feature A** (FR-01: Đăng ký tài khoản) | 25 | **25** | Thiết kế Domain + BVA, thực thi 11 TC và phát hiện 8 lỗi trong [Main_Report.md](./reports/Main_Report.md) |
| 2   | **Feature B** (FR-09: Áp dụng mã giảm giá) | 25 | **25** | Thiết kế Domain + BVA, thực thi 13 TC và phát hiện 5 lỗi trong [Main_Report.md](./reports/Main_Report.md) |
| 3   | **Feature C** (FR-14: Quản lý danh mục Admin) | 25 | **25** | Thiết kế Domain + BVA, thực thi 16 TC và phát hiện 6 lỗi trong [Main_Report.md](./reports/Main_Report.md) |
| 4   | **Feature D Mobile** (FR-02: Đăng nhập & Khóa di động) | 15 | **15** | Thiết kế Domain + BVA, thực thi 13 TC và phát hiện 5 lỗi trong [Main_Report.md](./reports/Main_Report.md) |
| 5   | **Agent Skills** (Custom AI Agent Skills) | 10 | **10** | Định nghĩa, cài đặt 5 skill tự động hóa kiểm thử trong [skills/](./skills/) và video demo |
|     | **TỔNG ĐIỂM** | **100** | **100** | **Đạt yêu cầu điểm tối đa (100/100)** |

---

## 3. Danh sách tính năng lựa chọn kiểm thử (Features Selected)

| Pool | Feature ID | Tên chức năng | Thành phần SUT | URL kiểm thử thực tế |
|------|------------|---------------|----------------|----------------------|
| **Pool A** | **FR-01** | Đăng ký tài khoản | Giao diện Web Client & API Backend | `http://localhost:5173/register` |
| **Pool B** | **FR-09** | Mã giảm giá (Discount coupon) | Giao diện Checkout Web & API Backend | `http://localhost:5173/checkout` |
| **Pool C** | **FR-14** | Quản lý danh mục (CRUD Category) | Giao diện Web Admin & API Backend | `http://localhost:5174` (Tab Danh mục) |
| **Pool D** | **FR-02** | Đăng nhập & Khóa tài khoản di động | Giao diện Mobile App & API Backend | Ứng dụng di động Expo Mobile (SUT) |

---

## 4. Tóm tắt kết quả kiểm thử (Test Summary Report)

Dưới đây là thống kê tổng hợp toàn bộ quá trình thiết kế, thực thi test case và báo cáo lỗi:

| Chỉ số kiểm thử (Test Metric) | Số lượng (Count) | Ghi chú |
|--------------------------------|------------------|---------|
| **Tổng số chức năng đã kiểm thử** | **4** | FR-01, FR-09, FR-14, FR-02 (Mobile) |
| **Tổng số Test Case đã thiết kế** | **59** | Thiết kế qua Domain Testing & BVA |
| **Tổng số Test Case đã thực thi** | **56** | Chạy kiểm thử tự động API & UI/Code Review |
| **Số Test Case ĐẠT (Passed)** | **21** | Logic hoạt động đúng đặc tả SRS |
| **Số Test Case KHÔNG ĐẠT (Failed)** | **35** | Do các lỗi/vấn đề không tuân thủ SRS |
| **Số Test Case chưa thực thi** | **3** | Các kịch bản thuộc giao diện confirmPassword thiếu trên web |
| **Tổng số lỗi phát hiện (Bugs Found)** | **24** | 8 lỗi FR-01, 5 lỗi FR-09, 6 lỗi FR-14, 5 lỗi FR-02-Mobile |

---

## 5. Video Demo (Demo Videos & Agent Skills)

Bấm vào đường dẫn dưới đây để xem video demo quy trình kiểm thử tự động, tích hợp AI Assistant (Antigravity AI Coding Assistant) và chạy các skill:

- **Link YouTube Demo:** [https://www.youtube.com/watch?v=O5KJnYe6VOs](https://www.youtube.com/watch?v=O5KJnYe6VOs)

Các skill của Agent được định nghĩa và triển khai đầy đủ bao gồm:
1. `hw02-workflow`: Quản lý toàn bộ quy trình kiểm thử tự động từ đọc đặc tả, thiết kế test case đến chạy test và kết xuất báo cáo.
2. `hw02-domain-testing`: Tự động thiết kế test case sử dụng kỹ thuật Phân vùng tương đương & Phân tích miền giá trị.
3. `hw02-boundary-value-analysis`: Thiết kế kiểm thử biên (BVA) & Robustness testing.
4. `hw02-bug-report`: Tổng hợp và tạo tệp báo cáo lỗi tích hợp liên kết hình ảnh trực quan.
5. `hw02-ai-audit-report`: Tự động ghi nhận lịch sử tương tác AI Audit Log sạch sẽ, trung thực.

---

## 6. Cấu trúc thư mục báo cáo

Toàn bộ tài liệu báo cáo của bài làm được tổ chức khoa học trong thư mục [reports/](./reports/):
- **[Main_Report.md](./reports/Main_Report.md):** Báo cáo kiểm thử chính. Chứa toàn bộ các bước thiết kế Domain Testing, Phân tích giá trị biên BVA, Nhật ký thực thi kiểm thử thực tế và phân tích khoảng cách AI (AI Gap Analysis - đã tinh chỉnh loại bỏ các phần giả định, chỉ giữ lại các phân tích lỗi bảo mật/logic thực tế mà AI đã bỏ sót).
- **[Bug_Report.md](./reports/Bug_Report.md):** Báo cáo lỗi hợp nhất. Mô tả chi tiết 24 lỗi phát hiện kèm theo câu lệnh PowerShell tái hiện cụ thể, expected/actual result, link issue tương ứng và bằng chứng ảnh chụp lỗi.
- **[AI_Critique.md](./reports/AI_Critique.md):** Bản tự kiểm và nhận xét quá trình sử dụng AI: chỉ ra những sai sót, thiên lệch giả định của AI, nguyên nhân bỏ sót lỗi thực tế và bài học kinh nghiệm thu được khi cộng tác với AI.
- **[AI_Audit_Report.md](./reports/AI_Audit_Report.md):** Tệp ghi nhận nhật ký kiểm toán tương tác với AI Assistant từ Interaction 001 đến Interaction 013 một cách trung thực.
- **[git_commit_log.txt](./reports/git_commit_log.txt):** Lịch sử commit Git trong suốt quá trình làm bài.
- **[FR-01_bugs/](./reports/FR-01_bugs/)**: Thư mục chứa các ảnh chụp bằng chứng lỗi của tính năng Đăng ký.
- **[FR-09_bugs/](./reports/FR-09_bugs/)**: Thư mục chứa các ảnh chụp bằng chứng lỗi của tính năng Mã giảm giá.
- **[FR-14_bugs/](./reports/FR-14_bugs/)**: Thư mục chứa các ảnh chụp bằng chứng lỗi của tính năng CRUD Danh mục (do sinh viên chụp).
- **[FR-02-mobile_bugs/](./reports/FR-02-mobile_bugs/)**: Thư mục chứa các ảnh chụp bằng chứng lỗi của tính năng Đăng nhập di động (do sinh viên chụp, hỗ trợ nhiều ảnh a/b cho lỗi attempts).

---

## 7. Liên kết Repository & Đóng góp
- **GitHub Issues:** [hungtmh/HW02-Domain_Testing/issues](https://github.com/hungtmh/HW02-Domain_Testing/issues)
  - Toàn bộ 24 Issues phát hiện đều đã được đẩy lên GitHub từ số #3 đến #26. Các issue này đều được liên kết trực tiếp bằng chứng hình ảnh thực tế tự động từ xa.
