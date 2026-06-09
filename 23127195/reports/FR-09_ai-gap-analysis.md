# AI Gap Analysis — FR-09: Mã Giảm Giá & Thanh Toán

**MSSV:** 23127195  
**Ngày:** 2026-06-09  

---

## 1. Những lỗi và kịch bản kiểm thử AI thông thường bỏ sót (AI Gaps)

Khi chỉ sử dụng những câu prompt chung chung (như *"kiểm thử chức năng discount"* hoặc *"viết test case áp dụng mã giảm giá"*), AI thường có xu hướng bỏ sót các kịch bản thực tế quan trọng:

| Kịch bản kiểm thử / Lỗi bị bỏ sót | Lý do AI bỏ sót (Root cause of AI gap) | Bài học rút ra & Giải pháp khắc phục |
|-----------------------------------|----------------------------------------|-------------------------------------|
| **1. Chặn sai logic biên dưới đơn hàng tối thiểu (BUG-001)** | AI mặc định giả định dev đã viết đúng logic so sánh `>=` của SRS. Nó ít khi tự viết test case kiểm tra biên chính xác bằng giá trị ngưỡng `total_amount = min_order_amount`. | Buộc AI phải viết các test case biên BVA cụ thể cho các điểm `Min - 1`, `Min`, `Min + 1` dựa trên cấu trúc database thực tế. |
| **2. Công thức tính toán phần trăm discount sai nghiêm trọng (BUG-002)** | AI thường tin tưởng tuyệt đối vào các phép tính số học cơ bản trong code. Nó thường chỉ viết kết quả mong đợi là "giảm 10%" mà không so khớp với công thức thực tế trong file backend `server.js` dòng 400. | Yêu cầu AI kiểm tra tĩnh công thức toán học được cài đặt trong code và chạy thử với dữ liệu đại diện để phát hiện sai lệch tính toán. |
| **3. API apply-coupon thiếu xác thực JWT (BUG-003)** | AI chỉ tập trung vào chức năng (Functional Testing) của mã giảm giá mà bỏ quên kiểm tra bảo mật (Security testing) đối với API endpoint xem nó có được bảo vệ bởi middleware xác thực hay không. | Ràng buộc AI phải phân tích các API endpoint xem có sử dụng middleware bảo mật (như `authenticateToken`) hay không. |
| **4. Giả mạo ID người dùng trong request body (BUG-004)** | AI có thói quen tin cậy thông tin đầu vào từ body và bỏ qua việc kiểm tra chéo (cross-verification) giữa thông tin định danh của JWT và dữ liệu body gửi lên. | Tạo thói quen kiểm thử bảo mật (Security Audit / Access Control), yêu cầu AI giả lập các request giả mạo ID người dùng khác xem server có chặn được không. |
| **5. Sửa đổi tổng tiền thanh toán tùy ý trên UI & API (BUG-005)** | AI giả định UI và API luôn đồng bộ và trường tổng tiền là chỉ đọc. Nó bỏ qua kịch bản kiểm thử thâm nhập (Penetration testing) bằng cách cố tình chỉnh sửa input value hoặc gửi API checkout giả mạo với số tiền 1 ₫. | Đưa kịch bản kiểm thử bypass giá trị (Parameter Tampering) vào danh mục test case tiêu chuẩn, yêu cầu AI kiểm tra tính toàn vẹn dữ liệu từ client lên server. |

---

## 2. Cách cải tiến prompt để tối ưu hóa AI trong kiểm thử phần mềm

Để khắc phục các lỗ hổng của AI ở trên, khi ra lệnh cho AI thiết kế test case, ta nên áp dụng các quy tắc prompt sau:

1. **Prompt yêu cầu kiểm tra tĩnh công thức toán học và logic so sánh:**
   * *❌ Tránh:* "Thiết kế test case áp dụng coupon."
   * *✔ Nên dùng:* "Đọc mã nguồn xử lý tính toán giảm giá của API [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js). Phân tích kỹ logic so sánh số tiền tối thiểu và công thức tính toán số tiền được giảm đối với từng loại coupon (fixed và percent). Chỉ ra xem có dòng code nào tính toán sai lệch so với SRS hay không."
2. **Prompt định hướng kiểm thử an ninh (Security & Access Control):**
   * *✔ Nên dùng:* "Với mỗi API endpoint liên quan đến tiền bạc hoặc thông tin người dùng (như apply-coupon, checkout), hãy thiết kế test case kiểm tra: (1) Request không gửi kèm Authorization Token; (2) Request gửi kèm Token của User A nhưng gửi parameters body của User B; (3) Request thay đổi các tham số nhạy cảm như giá tiền, trạng thái đơn hàng."
3. **Prompt kiểm thử hộp xám (Grey-box testing) kết hợp giao diện và dữ liệu:**
   * *✔ Nên dùng:* "Hãy rà soát file giao diện [Checkout.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Checkout.jsx) và chỉ ra các ô nhập liệu (input fields) nào cho phép người dùng sửa đổi trực tiếp. Kiểm tra xem backend tương ứng có tự động tính toán lại và xác thực các giá trị này không."
