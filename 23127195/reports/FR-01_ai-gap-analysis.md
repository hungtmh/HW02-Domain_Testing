# AI Gap Analysis — FR-01: Đăng ký tài khoản

**MSSV:** 23127195  
**Ngày:** 2026-06-09  

---

## 1. Những lỗi và kịch bản kiểm thử AI thông thường bỏ sót (AI Gaps)

Khi chỉ sử dụng những câu prompt chung chung (như *"viết test case đăng ký"* hoặc *"kiểm thử trang register"*), AI thường có xu hướng bỏ sót các kịch bản thực tế quan trọng:

| Kịch bản kiểm thử / Lỗi bị bỏ sót | Lý do AI bỏ sót (Root cause of AI gap) | Bài học rút ra & Giải pháp khắc phục |
|-----------------------------------|----------------------------------------|-------------------------------------|
| **1. Thiếu trường Xác nhận mật khẩu trên UI (BUG-005)** | AI có thói quen đọc tài liệu yêu cầu (SRS) và tự suy luận ra test case mà không chủ động đối chiếu mã nguồn thực tế của giao diện Frontend ([Register.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Register.jsx)). | Yêu cầu AI bắt buộc phải đọc mã nguồn UI trước khi thiết kế các test case ở mức giao diện. |
| **2. Regex mật khẩu mạnh bị sai, yêu cầu khoảng trắng (BUG-006)** | AI thường tin tưởng tuyệt đối rằng các biểu thức chính quy (Regex) trong mã nguồn đã được dev viết đúng theo đặc tả SRS. | Cần prompt AI thực hiện phân tích tĩnh (Static Analysis) đối với Regex thực tế trong code và tự so khớp với tập ký tự của SRS. |
| **3. Backend API hoàn toàn không validate dữ liệu (BUG-003, BUG-004)** | AI có xu hướng tập trung kiểm thử hộp đen (Black-box testing) trên giao diện Web mà quên mất việc kiểm thử API trực tiếp (API Bypass). | Phải yêu cầu AI lập hai danh sách test case riêng biệt: Client-side validation và Server-side API validation. |
| **4. Database cho phép trùng Email (BUG-001)** | AI mặc định giả định rằng cơ sở dữ liệu luôn được thiết kế tối ưu với các ràng buộc duy nhất (`UNIQUE`). | Ép buộc AI đọc file cấu hình database schema ([database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js)) trước khi kết luận về tính độc bản của dữ liệu. |
| **5. Lưu trữ mật khẩu dạng Plaintext (BUG-009)** | Lỗi này nằm ở mức phân tích an toàn thông tin (Security Audit). AI thông thường chỉ tập trung vào kiểm thử chức năng (Functional Testing). | Cần tích hợp thêm bước rà soát bảo mật (Security review) vào luồng làm việc tiêu chuẩn. |

---

## 2. Cách cải tiến prompt để tối ưu hóa AI trong kiểm thử phần mềm

Để khắc phục các lỗ hổng của AI ở trên, khi ra lệnh cho AI thiết kế test case, ta nên áp dụng các quy tắc prompt sau:

1. **Prompt định hướng đọc mã nguồn:**
   * *❌ Tránh:* "Thiết kế test case cho chức năng đăng ký tài khoản."
   * *✔ Nên dùng:* "Đọc mục FR-01 trong `README.md`. Sau đó đối chiếu với mã nguồn [Register.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Register.jsx) và [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js). Liệt kê những điểm sai khác giữa logic cài đặt thực tế và đặc tả yêu cầu."
2. **Prompt phân tách tầng kiểm thử (Layer-based testing):**
   * *✔ Nên dùng:* "Hãy thiết kế test case thành 2 phần: (1) Kiểm thử trên giao diện người dùng (UI) bao gồm cả thuộc tính HTML và CSS; (2) Kiểm thử API độc lập (bằng cách gửi payload JSON trực tiếp lên server để bypass frontend validation)."
3. **Prompt phân tích biên thực tế:**
   * *✔ Nên dùng:* "Phân tích giá trị biên (BVA) cho độ dài mật khẩu bằng cách kiểm thử chính xác các giá trị độ dài 7, 8, 9 ký tự. Đồng thời viết rõ kết quả kỳ vọng cho từng trường hợp thiếu chữ hoa, chữ thường, số, và ký tự đặc biệt."
