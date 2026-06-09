# AI Critique — HW02

Trong quá trình thực hiện bài tập lớn HW02 về Domain Testing trên hệ thống EShop, việc cộng tác với các công cụ AI (Cursor và Antigravity) đã bộc lộ rõ cả ưu điểm và những hạn chế nghiêm trọng về tính chính xác:

### 1. Sai sót và thiên lệch của AI (Gaps & Biases)
* **Thiên lệch giả định (Assumption Bias):** AI có xu hướng mặc định rằng mã nguồn thực tế đã được cài đặt hoàn toàn đúng theo tài liệu yêu cầu (SRS). Ví dụ, AI mặc định tin rằng Regex validate mật khẩu ở Frontend đã được viết đúng, hoặc Database chắc chắn đã được cấu hình ràng buộc `UNIQUE` cho cột email.
* **Bỏ sót tầng tích hợp:** Nếu không được nhắc nhở cụ thể, AI thường chỉ thiết kế test case cho giao diện (Black-box UI) mà bỏ quên hoàn toàn việc kiểm thử API (Backend API Bypass) hoặc rà soát cơ sở dữ liệu.

### 2. Nguyên nhân AI bỏ sót lỗi
* **Giới hạn về phạm vi quan sát (Context Window):** AI chỉ đọc các file khi được yêu cầu trực tiếp hoặc chỉ tập trung vào tài liệu đặc tả SRS mà không chủ động tìm kiếm các file code liên quan ở các component khác (như database schema hay file router).
* **Độ phức tạp của nghiệp vụ chéo:** AI gặp khó khăn trong việc phát hiện ra các lỗi logic phát sinh do sự phối hợp không đồng bộ giữa Frontend và Backend (Frontend validate nhưng Backend bỏ ngỏ).

### 3. Bài học rút ra khi cộng tác với AI
* **Không tin tưởng mù quáng (Trust but Verify):** Mọi kết quả do AI sinh ra (từ kịch bản kiểm thử cho tới kết quả phân vùng) bắt buộc phải được lập trình viên/tester rà soát thủ công (Human Review).
* **Kỹ thuật Prompt theo tầng (Layered Prompting):** Để AI hoạt động hiệu quả, cần phân rã yêu cầu thành các bước nhỏ hơn (Workflow): Yêu cầu đọc code trước, phân tích nghiệp vụ, sau đó mới sinh kịch bản test và yêu cầu kiểm thử API độc lập.
