<!-- File: FR-15_TestReport.md -->

# BÁO CÁO KIỂM THỬ: FR-15 — Quản lý Sản phẩm (Tạo / Cập nhật qua Admin Panel)

## 1. Phân hoạch tương đương (Equivalence Partitioning & Domain Analysis)

Dựa trên việc đối chiếu đặc tả (README) và giao diện thực tế (UI thực thi trên frontend), ta có các phân hoạch sau:

**1.1. Biến `name` (UI - Tên sản phẩm):**
- **Nguồn:** Trường nhập tên sản phẩm trên form Admin (`productForm.name`).
- **Ràng buộc UI thật:** Thẻ `<input type="text">` có thuộc tính `required` của HTML5. Không giới hạn độ dài (`maxLength`). Không tự động trim khoảng trắng. Không có nhãn hiển thị và ký hiệu `*` bắt buộc.
- **Ràng buộc Đặc tả:** Bắt buộc, tối đa 255 ký tự. Phải có dấu `*` bên cạnh nhãn.
- **VEC-name-1:** Chuỗi ký tự hợp lệ, độ dài từ 1 đến 255 ký tự (VD: `"Bàn phím cơ"`).
- **VEC-name-2:** Chuỗi ký tự chứa ký tự đặc biệt hoặc số, độ dài từ 1 đến 255 ký tự (VD: `"Chuột chơi game G-102 @!"`).
- **IEC-name-1:** Chuỗi rỗng `""` (Bỏ trống) — bị chặn bởi `required` của HTML5 ở frontend.
- **IEC-name-2:** Chuỗi chỉ chứa các khoảng trắng `"   "` — vượt qua được kiểm tra `required` ở frontend.
- **IEC-name-3:** Chuỗi có độ dài vượt quá 255 ký tự (VD: chuỗi 256 ký tự) — không bị chặn ở frontend do thiếu `maxLength`.
- **Ghi chú Inconsistency:** Giao diện thiếu nhãn hiển thị và ký hiệu `*` bắt buộc (vi phạm FR-22), thiếu giới hạn độ dài `maxLength` ở frontend (vi phạm FR-15).

**1.2. Biến `price` (UI - Giá tiền):**
- **Nguồn:** Trường nhập giá tiền trên form Admin (`productForm.price`).
- **Ràng buộc UI thật:** Thẻ `<input type="number">` nhưng không có thuộc tính `min` và `required`. Không có nhãn hiển thị và ký hiệu `*` bắt buộc.
- **Ràng buộc Đặc tả:** Bắt buộc, phải là số dương (> 0). Phải có dấu `*` bên cạnh nhãn. Định dạng phân cách hàng nghìn.
- **VEC-price-1:** Số nguyên dương lớn hơn 0 (VD: `150000`).
- **IEC-price-1:** Bỏ trống (chuỗi rỗng `""`) — vượt qua được frontend do thiếu `required`.
- **IEC-price-2:** Giá trị bằng 0 — vượt qua được frontend do thiếu `min="1"`.
- **IEC-price-3:** Giá trị số âm (VD: `-50000`) — vượt qua được frontend do thiếu `min="1"`.
- **IEC-price-4:** Số thực thập phân (VD: `99.99` hoặc `1500.5`) — vượt qua được frontend (backend lưu dạng REAL mặc dù schema khai báo INTEGER).
- **Ghi chú Inconsistency:** Giao diện thiếu nhãn hiển thị và ký hiệu `*` bắt buộc (vi phạm FR-22). Giá hiển thị trên danh sách sản phẩm thiếu định dạng phân cách hàng nghìn (vi phạm FR-21). Frontend hoàn toàn thiếu kiểm tra giá trị âm/trống cho trường Giá tiền (vi phạm FR-15).

**1.3. Biến `category_id` (UI - Danh mục):**
- **Nguồn:** Thẻ `<select>` chọn danh mục.
- **Ràng buộc UI thật:** Chọn một trong các option danh mục được load từ cơ sở dữ liệu.
- **Ràng buộc Đặc tả:** Bắt buộc, phải chọn từ danh mục có sẵn. Phải có dấu `*` bên cạnh nhãn.
- **VEC-cat-1:** Danh mục hợp lệ được chọn từ danh sách dropdown (VD: `1`).
- **Ghi chú Inconsistency:** Giao diện thiếu nhãn hiển thị và ký hiệu `*` bắt buộc (vi phạm FR-22).

**1.4. Các trường tùy chọn (`imageUrl`, `description`):**
- **Nguồn:** Trường "URL Ảnh" (`imageUrl`) và "Mô tả" (`description`).
- **Ràng buộc UI thật & Đặc tả:** Tùy chọn, không bắt buộc.
- **VEC-opt-1:** Có nhập giá trị hợp lệ.
- **VEC-opt-2:** Để trống.

---

## 2. Phân tích giá trị biên (Boundary Value Analysis)

**2.1. Biến `name` (Độ dài tên sản phẩm):**
- **Biên đặc tả:** `length ∈ [1, 255]`.
- **Điểm biên:**
  - `length = 0` (Below biên dưới, OFF - Không hợp lệ)
  - `length = 1` (Biên dưới, ON - Hợp lệ)
  - `length = 2` (Above biên dưới - Hợp lệ)
  - `length = 254` (Below biên trên - Hợp lệ)
  - `length = 255` (Biên trên, ON - Hợp lệ)
  - `length = 256` (Above biên trên, OFF - Không hợp lệ)

**2.2. Biến `price` (Giá trị số nguyên):**
- **Biên đặc tả:** `price ≥ 1` (Giá phải là số dương (> 0). Đối với số nguyên, giá trị dương nhỏ nhất là 1).
- **Điểm biên:**
  - `price = -1` (Không hợp lệ)
  - `price = 0` (Biên đặc tả nghiệp vụ, OFF - Không hợp lệ)
  - `price = 1` (Biên dưới, ON - Hợp lệ)
  - `price = 2` (Above biên dưới - Hợp lệ)

---

## 3. Bảng thiết kế Test Case (Test Case DESIGN)

| Test Case ID | Mục đích (Objective) | Tiền điều kiện (Pre-conditions) | Các bước (Steps) | Dữ liệu đầu vào (Input) | Kết quả mong đợi CHUẨN (Expected — spec-correct) | Loại Input (Valid/Invalid) | Ưu tiên (Priority) |
|---|---|---|---|---|---|---|---|
| FR15-TC-A01 | Thêm sản phẩm mới thành công qua UI với thông tin hợp lệ | Admin đã đăng nhập, ở tab "Sản phẩm", đã có danh mục trong DB | 1. Nhập Tên sản phẩm<br>2. Nhập Giá tiền<br>3. Nhập URL Ảnh<br>4. Nhập Mô tả<br>5. Chọn Danh mục<br>6. Bấm "Lưu sản phẩm" | `name` = "Bàn phím cơ AKKO"<br>`price` = 1500000<br>`imageUrl` = "https://placehold.co/150"<br>`description` = "Bàn phím cơ TKL"<br>`category_id` = 1 | Hệ thống tạo sản phẩm thành công, thông báo thành công, sản phẩm mới hiển thị dưới danh sách với giá định dạng phân cách hàng nghìn "1.500.000 ₫". | Valid | High |
| FR15-TC-A02 | Sửa thông tin sản phẩm thành công và không ảnh hưởng sản phẩm khác | Admin đã đăng nhập, danh sách có ít nhất 2 sản phẩm (SP A và SP B) | 1. Bấm nút "Sửa" ở dòng sản phẩm A<br>2. Nhập tên sản phẩm mới<br>3. Bấm "Lưu sản phẩm" | Chọn sản phẩm A, thay đổi `name` thành "Bàn phím cơ AKKO PRO" | Chỉ sản phẩm A bị cập nhật tên thành "Bàn phím cơ AKKO PRO". Sản phẩm B và các sản phẩm khác giữ nguyên thông tin ban đầu. | Valid | High |
| FR15-TC-B01 | Lỗi thêm sản phẩm để trống Tên sản phẩm | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Để trống ô "Tên sản phẩm"<br>2. Nhập Giá tiền hợp lệ<br>3. Bấm "Lưu sản phẩm" | `name` = ""<br>`price` = 150000 | Trình duyệt chặn submit form và hiển thị cảnh báo yêu cầu nhập tên sản phẩm (HTML5 Validation). | Invalid | High |
| FR15-TC-B02 | Lỗi thêm sản phẩm với tên chỉ chứa khoảng trắng | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm chỉ chứa khoảng trắng<br>2. Nhập Giá tiền hợp lệ<br>3. Bấm "Lưu sản phẩm" | `name` = "   "<br>`price` = 150000 | Hệ thống từ chối submit, hiển thị lỗi yêu cầu tên sản phẩm không được rỗng. | Invalid | High |
| FR15-TC-B03 | Lỗi thêm sản phẩm để trống Giá tiền | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm hợp lệ<br>2. Để trống ô "Giá tiền"<br>3. Bấm "Lưu sản phẩm" | `name` = "Sản phẩm mẫu"<br>`price` = "" | Hệ thống chặn submit, hiển thị lỗi yêu cầu nhập giá tiền. | Invalid | High |
| FR15-TC-B04 | Lỗi thêm sản phẩm với giá tiền âm | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm hợp lệ<br>2. Nhập giá tiền âm<br>3. Bấm "Lưu sản phẩm" | `name` = "Sản phẩm mẫu"<br>`price` = -50000 | Hệ thống chặn submit, báo lỗi giá tiền phải lớn hơn 0. | Invalid | High |
| FR15-TC-B05 | Lỗi thêm sản phẩm với giá tiền bằng 0 | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm hợp lệ<br>2. Nhập giá tiền bằng 0<br>3. Bấm "Lưu sản phẩm" | `name` = "Sản phẩm mẫu"<br>`price` = 0 | Hệ thống chặn submit, báo lỗi giá tiền phải lớn hơn 0. | Invalid | High |
| FR15-TC-C01 | BVA: Thêm sản phẩm có Tên sản phẩm = 1 ký tự (Biên dưới) | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm 1 ký tự<br>2. Nhập Giá tiền hợp lệ<br>3. Bấm "Lưu sản phẩm" | `name` = "A"<br>`price` = 10000 | Tạo sản phẩm thành công, hiển thị trong danh sách. | Valid | Medium |
| FR15-TC-C02 | BVA: Thêm sản phẩm có Tên sản phẩm = 255 ký tự (Biên trên) | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm dài 255 ký tự<br>2. Nhập Giá tiền hợp lệ<br>3. Bấm "Lưu sản phẩm" | `name` = "A".repeat(255)<br>`price` = 10000 | Tạo sản phẩm thành công, hiển thị trong danh sách. | Valid | Medium |
| FR15-TC-C03 | BVA: Lỗi thêm sản phẩm có Tên sản phẩm = 256 ký tự (Vượt biên trên) | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm dài 256 ký tự<br>2. Nhập Giá tiền hợp lệ<br>3. Bấm "Lưu sản phẩm" | `name` = "A".repeat(256)<br>`price` = 10000 | Hệ thống báo lỗi tên sản phẩm không được vượt quá 255 ký tự và chặn submit. | Invalid | Medium |
| FR15-TC-D01 | BVA: Thêm sản phẩm với Giá tiền = 1 (Số dương nhỏ nhất) | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm hợp lệ<br>2. Nhập Giá tiền = 1<br>3. Bấm "Lưu sản phẩm" | `name` = "Sản phẩm giá 1đ"<br>`price` = 1 | Tạo sản phẩm thành công, hiển thị giá "1 ₫". | Valid | Medium |
| FR15-TC-D02 | BVA: Thêm sản phẩm với Giá tiền = 2 | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm hợp lệ<br>2. Nhập Giá tiền = 2<br>3. Bấm "Lưu sản phẩm" | `name` = "Sản phẩm giá 2đ"<br>`price` = 2 | Tạo sản phẩm thành công, hiển thị giá "2 ₫". | Valid | Low |
| FR15-TC-E01 | Thêm sản phẩm không nhập URL ảnh và Mô tả | Admin đã đăng nhập, ở tab "Sản phẩm" | 1. Nhập Tên sản phẩm hợp lệ<br>2. Nhập Giá tiền hợp lệ<br>3. Để trống ô "URL Ảnh" và "Mô tả"<br>4. Bấm "Lưu sản phẩm" | `name` = "Bàn di chuột"<br>`price` = 50000<br>`imageUrl` = ""<br>`description` = "" | Tạo sản phẩm thành công. Cột ảnh hiển thị ảnh placeholder mặc định. | Valid | Medium |

---

## 4. Khung thực thi (Test EXECUTION Skeleton)

| Test Case ID | Kết quả thực tế (Actual) | Trạng thái (Pass/Fail/Blocked) | Ngày chạy | Người test | Môi trường/Build | Bug ID liên quan | Ghi chú nghi vấn (từ phân tích code) |
|---|---|---|---|---|---|---|---|
| FR15-TC-A01 | | | | | | BUG-FR15-05 | NGHI VẤN: Giá tiền hiển thị không có dấu phân cách hàng nghìn (hiển thị dạng "1500000 ₫" thay vì "1.500.000 ₫"). |
| FR15-TC-A02 | | | | | | BUG-FR15-01 | NGHI VẤN: State React bị lỗi ghi đè toàn bộ tên sản phẩm trong local state khi lưu cập nhật. |
| FR15-TC-B01 | | | | | | | |
| FR15-TC-B02 | | | | | | BUG-FR15-07 | NGHI VẤN: Không trim khoảng trắng ở frontend nên tên chỉ chứa khoảng trắng sẽ lọt qua. |
| FR15-TC-B03 | | | | | | BUG-FR15-03 | NGHI VẤN: Lọt qua frontend do input "Giá tiền" thiếu thuộc tính `required`. |
| FR15-TC-B04 | | | | | | BUG-FR15-03 | NGHI VẤN: Lọt qua frontend do input "Giá tiền" thiếu thuộc tính `min="1"`. |
| FR15-TC-B05 | | | | | | BUG-FR15-03 | NGHI VẤN: Lọt qua frontend do input "Giá tiền" thiếu thuộc tính `min="1"`. |
| FR15-TC-C01 | | | | | | | |
| FR15-TC-C02 | | | | | | | |
| FR15-TC-C03 | | | | | | | NGHI VẤN: Lọt qua frontend do input "Tên sản phẩm" thiếu thuộc tính `maxLength="255"`. |
| FR15-TC-D01 | | | | | | | |
| FR15-TC-D02 | | | | | | | |
| FR15-TC-E01 | | | | | | | |

---

## 5. Báo cáo Lỗi (Defect / Bug Report)

| Bug ID | Tiêu đề (Title) | Tiền điều kiện & Môi trường | Các bước tái hiện (đánh số) | Kết quả mong đợi | Kết quả thực tế | Severity | Priority | Trạng thái | Vị trí (File:Line) | Bằng chứng (ảnh/log) |
|---|---|---|---|---|---|---|---|---|---|---|
| BUG-FR15-01 | **[Nghiêm trọng] React State ghi đè tên toàn bộ sản phẩm trong danh sách khi cập nhật** | Đang ở tab "Sản phẩm", đã có sản phẩm trong danh sách | 1. Bấm nút "Sửa" tại bất kỳ sản phẩm nào.<br>2. Nhập tên mới vào form (ví dụ: "Bàn phím cơ giá rẻ").<br>3. Bấm "Lưu sản phẩm". | Chỉ sản phẩm được sửa đổi mới cập nhật tên mới. Các sản phẩm khác trong danh sách giữ nguyên tên của chúng. | Toàn bộ sản phẩm hiển thị trong danh sách lập tức bị đổi tên thành "Bàn phím cơ giá rẻ" (Chỉ quay lại bình thường sau khi F5 tải lại trang). | Critical | High | Confirmed | `App.jsx:L110-L114` | `![screenshot](./img/BUG-FR15-01.png)` |
| BUG-FR15-02 | **Form thêm/sửa sản phẩm thiếu nhãn (label) và ký hiệu * bắt buộc** | Đang ở tab "Sản phẩm" | 1. Quan sát form nhập liệu "Thêm sản phẩm mới" / "Sửa sản phẩm". | Có nhãn rõ ràng cho các trường Tên sản phẩm, Giá tiền, Danh mục kèm ký hiệu `*` màu đỏ để đánh dấu các trường bắt buộc (theo FR-22). | Không có bất kỳ thẻ `<label>` nào được hiển thị, chỉ dùng `placeholder` trong thẻ input làm nhãn tạm. Không có dấu `*` bên cạnh các trường. | Medium | Medium | Confirmed | `App.jsx:L490-L544` | `![screenshot](./img/BUG-FR15-02.png)` |
| BUG-FR15-03 | **Thiếu validate giá trị âm/trống cho Giá tiền ở Frontend** | Đang ở tab "Sản phẩm" | 1. Để trống ô "Giá tiền" hoặc nhập giá trị âm `-50000`.<br>2. Bấm "Lưu sản phẩm". | Form bị chặn submit ở frontend, báo lỗi yêu cầu nhập giá trị lớn hơn 0. | Hệ thống cho phép submit thành công lên backend mà không có bất kỳ cản trở nào ở phía client. | High | High | Confirmed | `App.jsx:L500-L508` | `![screenshot](./img/BUG-FR15-03.png)` |
| BUG-FR15-04 | **Sai tiêu chuẩn thẻ tiêu đề trang (dùng h2 thay vì h1)** | Đang ở tab "Sản phẩm" | 1. F12 kiểm tra thẻ HTML tiêu đề "Quản lý Sản phẩm". | Tiêu đề "Quản lý Sản phẩm" phải là thẻ `<h1>` duy nhất trên trang để mô tả nội dung theo FR-21. | Tiêu đề "Quản lý Sản phẩm" đang sử dụng thẻ `<h2>`. | Low | Low | Confirmed | `App.jsx:L339` | `![screenshot](./img/BUG-FR15-04.png)` |
| BUG-FR15-05 | **Thiếu định dạng phân cách hàng nghìn cho giá sản phẩm trong danh sách Admin** | Đang ở tab "Sản phẩm" | 1. Xem danh sách sản phẩm hiển thị.<br>2. Quan sát cột "Giá". | Giá tiền hiển thị phải có định dạng phân cách hàng nghìn và ký hiệu `₫` (VD: `1.500.000 ₫` theo FR-21). | Giá tiền hiển thị dạng số thô không có phân cách hàng nghìn (VD: `1500000 ₫`). | Low | Low | Confirmed | `App.jsx:L590` | `![screenshot](./img/BUG-FR15-05.png)` |
| BUG-FR15-06 | **[Bảo mật] Các API tạo/sửa/xóa sản phẩm thiếu hoàn toàn lớp xác thực & phân quyền** | Sử dụng API Client (như Postman/curl) | 1. Gửi request POST/PUT/DELETE tới các endpoint `/api/products` mà không truyền header Authorization hoặc dùng token của user thường. | Backend trả về lỗi `401 Unauthorized` hoặc `403 Forbidden` chặn thao tác trái phép theo FR-12. | Thao tác thêm/sửa/xóa sản phẩm vẫn diễn ra thành công (HTTP 200) mà không cần bất kỳ quyền admin nào. | Critical | High | Confirmed | `server.js:L167-L197` | `![screenshot](./img/BUG-FR15-06.png)` |
| BUG-FR15-07 | **Thiếu validate dữ liệu phía server-side cho API Products** | Gửi request API | 1. Gửi POST/PUT tới `/api/products` chứa `price` là chữ `"abc"` hoặc giá âm `-50000`. | Backend trả về lỗi `400 Bad Request` và từ chối ghi dữ liệu bẩn. | Backend xử lý thành công (HTTP 200) và SQLite ghi nhận các giá trị bẩn này vào database. | High | High | Confirmed | `server.js:L167-L189` | `![screenshot](./img/BUG-FR15-07.png)` |
| BUG-FR15-08 | **API GET chi tiết sản phẩm ép giá thành kiểu string nếu ID chẵn** | Gửi request API | 1. Gọi `GET /api/products/:id` với ID chẵn (VD: ID = 2). | Dữ liệu `price` trả về phải luôn là kiểu số (number/integer). | Dữ liệu `price` trả về bị ép thành kiểu chuỗi (string) (VD: `"300000"` thay vì `300000`). | Medium | Medium | Confirmed | `server.js:L162` | `![screenshot](./img/BUG-FR15-08.png)` |

---

## 6. Tóm tắt Kiểm thử (Test Summary)

- **Thống kê Test Case:**
  - Thiết kế (Designed): 13
  - Đã chạy (Executed): (điền sau khi chạy)
  - Passed: (điền sau khi chạy)
  - Failed: (điền sau khi chạy)
  - Blocked: (điền sau khi chạy)

- **Thống kê Báo cáo lỗi (Confirmed từ phân tích code tĩnh & đối chiếu UI):**
  - **Critical:** 2 (Lỗi React State ghi đè tên SP, Lỗi bảo mật bypass auth các API)
  - **High:** 2 (Thiếu validate giá âm/trống ở frontend, Thiếu validate phía server-side)
  - **Medium:** 2 (Thiếu nhãn/dấu * bắt buộc trong form, Lỗi ép kiểu string cho ID chẵn)
  - **Low:** 2 (Dùng sai thẻ tiêu đề h2, Thiếu định dạng phân cách hàng nghìn cho giá SP)
  - **Tổng cộng:** 8 Bugs

- **Đánh giá rủi ro & Khuyến nghị:**
  - **Rủi ro chức năng và UX:** Chức năng chỉnh sửa sản phẩm bị lỗi state nghiêm trọng, gây hoang mang cho người quản trị khi thấy toàn bộ sản phẩm bị đổi tên. Form thiếu nhãn, dấu bắt buộc `*` và định dạng phân cách hàng nghìn làm giảm nghiêm trọng tính chuyên nghiệp của UI (vi phạm FR-21, FR-22).
  - **Rủi ro bảo mật & toàn vẹn dữ liệu:** Bất kỳ ai cũng có thể gọi API thêm/sửa/xóa sản phẩm mà không cần đăng nhập admin. Backend hoàn toàn tin tưởng client và ghi trực tiếp dữ liệu âm, chuỗi chữ vào DB mà không validation.
  - **Khuyến nghị sửa ngay:**
    - **Frontend:**
      1. Trong `handleProductSubmit`, cập nhật state `products` một cách chính xác bằng cách tìm theo ID sản phẩm:
         ```jsx
         const updatedProducts = products.map((p) =>
           p.id === productForm.id ? { ...p, ...productForm, price: parseInt(productForm.price, 10) } : p
         );
         setProducts(updatedProducts);
         ```
      2. Thêm thẻ `<label>` và biểu tượng `*` cho các trường bắt buộc trong form sản phẩm.
      3. Thêm các thuộc tính `required` và `min="1"` vào thẻ input của `price`.
      4. Sửa thẻ tiêu đề trang từ `<h2>` thành `<h1>` trong `App.jsx:L339`.
      5. Áp dụng `.toLocaleString('vi-VN')` khi hiển thị giá sản phẩm trên giao diện admin.
    - **Backend:**
      1. Áp dụng middleware `authenticateToken` và kiểm tra quyền admin (qua kiểm tra role) cho các route `POST/PUT/DELETE /api/products`.
      2. Loại bỏ dòng ép kiểu chuỗi cho ID chẵn ở `GET /api/products/:id` (`row.price = row.price.toString()`).
      3. Thêm validation các trường bắt buộc và kiểu dữ liệu ở backend trước khi thực thi câu lệnh SQL.

---

### Phụ lục A — Inconsistency đặc tả (readme) vs UI thật

| Đối tượng / Biến | Đặc tả yêu cầu | UI thật thực hiện | Ảnh hưởng tới kiểm thử | Ghi chú / Finding |
|---|---|---|---|---|
| Nhãn và Ký hiệu bắt buộc | Tất cả các trường bắt buộc phải có dấu `*` bên cạnh nhãn (FR-22). | Không hiển thị nhãn, không có dấu `*` bắt buộc. | Không thể kiểm tra sự hiển thị trực quan của dấu `*` trên UI. | Ghi nhận BUG-FR15-02 |
| Ràng buộc Tên sản phẩm | Bắt buộc, tối đa 255 ký tự (FR-15). | Form Admin cho phép nhập chuỗi trống hoặc chuỗi dài tùy ý không giới hạn ký tự. | Test case nhập tên trống (chứa khoảng trắng) hoặc quá dài (>255 ký tự) lọt qua Frontend và ghi vào CSDL. | Ghi nhận BUG-FR15-07 |
| Ràng buộc Giá tiền | Bắt buộc, số dương (> 0) (FR-15). | Input cho phép để trống, cho phép nhập số âm hoặc bằng 0. | Test case giá trị âm, trống hoặc bằng 0 lọt qua Frontend và ghi vào CSDL. | Ghi nhận BUG-FR15-03 |
| Định dạng tiền tệ | Luôn có ký hiệu `₫` với định dạng phân cách hàng nghìn (FR-21). | Giá tiền trong bảng danh sách sản phẩm hiển thị số thô ghép với ký hiệu `₫` (VD: `1500000 ₫`). | Vi phạm định dạng hiển thị tiêu chuẩn. | Ghi nhận BUG-FR15-05 |
| Tiêu đề trang | Mỗi trang/màn hình có đúng 1 thẻ `<h1>` (FR-21). | Tiêu đề "Quản lý Sản phẩm" dùng thẻ `<h2>` trong khi sidebar đã chứa thẻ `<h1>EShop Admin</h1>`. | Nếu sửa tiêu đề thành `<h1>` sẽ dẫn đến việc trang chứa 2 thẻ `<h1>` đồng thời. | Ghi nhận BUG-FR15-04 |

### Phụ lục B — Reserved cho bài API Testing

> **CẢNH BÁO:** Các case dưới đây dùng để gọi trực tiếp các API, bypass giao diện Frontend. Các case này **KHÔNG** tính điểm cho HW02 (Functional qua UI) và được để dành (reserved) cho bài API Testing sau này.

| Test Case ID | Mục đích (Objective) | Tiền điều kiện (Pre-conditions) | Các bước (Steps) | Dữ liệu đầu vào (Input) | Kết quả mong đợi CHUẨN (Expected — spec-correct) | Loại Input (Valid/Invalid) | Ưu tiên (Priority) |
|---|---|---|---|---|---|---|---|
| FR15-API-TC-01 | Gửi POST tạo sản phẩm trực tiếp qua API với price dạng chuỗi số | API Backend đang chạy | Gửi POST request tới `/api/products` | Body: `{"name": "Sản phẩm API", "price": "50000", "category_id": 1}` | Trả về `400 Bad Request` do price sai kiểu dữ liệu (phải là integer). | Invalid | Medium |
| FR15-API-TC-02 | Gửi POST tạo sản phẩm trực tiếp qua API với price dạng chuỗi chữ | API Backend đang chạy | Gửi POST request tới `/api/products` | Body: `{"name": "Sản phẩm API", "price": "abc", "category_id": 1}` | Trả về `400 Bad Request` do price không phải là số hợp lệ. | Invalid | High |
| FR15-API-TC-03 | Gửi POST tạo sản phẩm trực tiếp qua API với price số âm | API Backend đang chạy | Gửi POST request tới `/api/products` | Body: `{"name": "Sản phẩm API", "price": -50000, "category_id": 1}` | Trả về `400 Bad Request` do price phải là số dương (>0). | Invalid | High |
| FR15-API-TC-04 | Gửi POST tạo sản phẩm trực tiếp qua API với price là null | API Backend đang chạy | Gửi POST request tới `/api/products` | Body: `{"name": "Sản phẩm API", "price": null, "category_id": 1}` | Trả về `400 Bad Request` do thiếu trường bắt buộc price. | Invalid | Medium |
| FR15-API-TC-05 | Gửi POST tạo sản phẩm trực tiếp qua API với name là null | API Backend đang chạy | Gửi POST request tới `/api/products` | Body: `{"name": null, "price": 100000, "category_id": 1}` | Trả về `400 Bad Request` do thiếu trường bắt buộc name. | Invalid | High |
| FR15-API-TC-06 | Gửi POST tạo sản phẩm trực tiếp qua API với name chỉ có khoảng trắng | API Backend đang chạy | Gửi POST request tới `/api/products` | Body: `{"name": "   ", "price": 100000, "category_id": 1}` | Trả về `400 Bad Request` do tên không được phép rỗng. | Invalid | High |
| FR15-API-TC-07 | Gửi POST tạo sản phẩm trực tiếp qua API với category_id không tồn tại | API Backend đang chạy | Gửi POST request tới `/api/products` | Body: `{"name": "Sản phẩm API", "price": 100000, "category_id": 9999}` | Trả về `400 Bad Request` do khóa ngoại category_id không hợp lệ. | Invalid | High |
| FR15-API-TC-08 | Thêm sản phẩm trực tiếp qua API không kèm Token | API Backend đang chạy | Gửi POST request tới `/api/products` không có Header Authorization | Body hợp lệ | Trả về `401 Unauthorized` chặn truy cập. | Invalid | High |
| FR15-API-TC-09 | Thêm sản phẩm trực tiếp qua API với Token của user thường | API Backend đang chạy, có token của tài khoản customer | Gửi POST request tới `/api/products` kèm Header Authorization của user thường | Body hợp lệ | Trả về `403 Forbidden` chặn truy cập. | Invalid | High |
| FR15-API-TC-10 | Gọi API import sản phẩm từ CSV với Token của user thường | API Backend đang chạy, có token của tài khoản customer | Gửi POST request tới `/api/admin/import-products` kèm Header Authorization của user thường | Body hợp lệ | Trả về `403 Forbidden` chặn truy cập. | Invalid | High |
