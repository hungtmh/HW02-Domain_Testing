<!-- File: FR-03_TestReport.md -->

# BÁO CÁO KIỂM THỬ: FR-03 (Quên mật khẩu & Đặt lại mật khẩu)

## 1. Phân hoạch tương đương (Equivalence Partitioning & Domain Analysis)

Dựa trên việc đối chiếu đặc tả (README) và giao diện thực tế (UI thực thi trên frontend), ta có các phân hoạch sau:

**1.1. Biến `email` (UI - Bước 1):**

- **Nguồn:** Trường nhập liệu ở Bước 1.
- **Ràng buộc UI thật:** Thẻ `<input type="text">` (chấp nhận mọi chuỗi, không validate format HTML5).
- **Ràng buộc Đặc tả:** Email hợp lệ, duy nhất, đã tồn tại trong hệ thống.
- **VEC-email-1:** Chuỗi đúng định dạng email và tồn tại trong DB (VD: `test@eshop.com`).
- **IEC-email-1:** Chuỗi sai định dạng email (VD: `test.com`).
- **IEC-email-2:** Chuỗi đúng định dạng nhưng không tồn tại trong DB (VD: `notfound@eshop.com`).
- **IEC-email-3:** Bỏ trống.
- **Ghi chú Inconsistency:** Giao diện vi phạm FR-22 (dùng `type="text"`, thiếu dấu `*`).

**1.2. Biến `resetToken` (UI - Bước 2):**

- **Nguồn:** Trường nhập OTP.
- **Ràng buộc UI thật:** Giao diện ghi rõ "Mã OTP (4 số)". Backend sinh mã 4 chữ số.
- **VEC-otp-1:** Chuỗi 4 chữ số hợp lệ đúng với mã đã sinh (VD: `1234`).
- **IEC-otp-1:** Chuỗi 4 chữ số nhưng không khớp mã đã sinh (VD: `9999`).
- **IEC-otp-2:** Chứa ký tự chữ hoặc ký tự đặc biệt (VD: `123a`).
- **IEC-otp-3:** Bỏ trống.
- **Ghi chú Inconsistency:** Đặc tả yêu cầu 6 chữ số, nhưng UI ép nhập 4 chữ số (Thiết kế test theo UI 4 số, nhưng Expected sẽ đòi hỏi hệ thống báo lỗi hoặc hành vi theo spec 6 số).

**1.3. Biến `newPassword` (UI - Bước 2):**

- **Nguồn:** Trường Mật khẩu mới.
- **Ràng buộc UI thật:** Dựa vào code Frontend, regex yêu cầu `[A-Za-z\d\s]{8,}$` -> Bắt buộc có khoảng trắng, chữ hoa, chữ thường, số, và **CẤM** ký tự đặc biệt.
- **VEC-pwd-1:** Thỏa mãn regex của UI (VD: `Password 123`).
- **IEC-pwd-1:** Chứa ký tự đặc biệt, không có khoảng trắng (Đây là pass chuẩn đặc tả nhưng UI coi là invalid) (VD: `Test@1234`).
- **IEC-pwd-2:** Dưới 8 ký tự (VD: `P w 1`).
- **IEC-pwd-3:** Thiếu chữ hoa (VD: `password 123`).
- **IEC-pwd-4:** Thiếu chữ thường (VD: `PASSWORD 123`).
- **IEC-pwd-5:** Thiếu chữ số (VD: `Password abc`).
- **IEC-pwd-6:** Bỏ trống.
- **Ghi chú Inconsistency:** Logic kiểm tra của UI hoàn toàn ngược lại với đặc tả FR-01/FR-03 (cấm ký tự đặc biệt và ép dùng khoảng trắng).

**1.4. Biến `confirmPassword` (UI - Bước 2):**

- **Nguồn:** Lẽ ra phải là trường "Xác nhận mật khẩu mới".
- **Ghi chú Inconsistency:** Trường này **hoàn toàn bị thiếu** trên giao diện, dẫn đến không thể phân hoạch hay thực thi kiểm tra 2 mật khẩu có khớp nhau không. (Chuyển thành Bug Blocker).

---

## 2. Phân tích giá trị biên (Boundary Value Analysis)

**2.1. Biến `resetToken` (Độ dài):**

- **Biên (Theo UI):** 4 ký tự.
- **Điểm biên:**
  - `length = 3` (OFF)
  - `length = 4` (ON)
  - `length = 5` (OFF)

**2.2. Biến `newPassword` (Độ dài):**

- **Biên:** Tối thiểu 8 ký tự.
- **Điểm biên:**
  - `length = 7` (OFF)
  - `length = 8` (ON)
  - `length = 9` (Valid)

---

## 3. Bảng thiết kế Test Case (Test Case DESIGN)

| Test Case ID | Mục đích (Objective)                                                  | Tiền điều kiện (Pre-conditions) | Các bước (Steps)                                                                              | Dữ liệu đầu vào (Input)                                                                                        | Kết quả mong đợi CHUẨN (Expected — spec-correct)                         | Loại Input (Valid/Invalid) | Ưu tiên (Priority) |
| ------------ | --------------------------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------- | ------------------ |
| FR03-TC-A01  | Luồng chuẩn đặt lại mật khẩu thành công                               | Có tài khoản `test@eshop.com`   | 1. Nhập email (B1)<br>2. Nhập OTP và Pass mới chuẩn đặc tả (B2)<br>3. Nhập xác nhận Pass (B2) | `email`=`test@eshop.com`<br>`resetToken`=[OTP 6 số đúng]<br>`newPassword`=`Test1234!`<br>`confirm`=`Test1234!` | Ở Bước 2, đổi pass thành công, hệ thống chuyển hướng về trang Đăng nhập. | Valid                      | High               |
| FR03-TC-B01  | Lỗi email sai định dạng                                               | Đang ở trang Quên pass (B1)     | Nhập email sai định dạng & Submit                                                             | `email`=`test.com`                                                                                             | Trình duyệt báo lỗi HTML5 (Vui lòng nhập định dạng email).               | Invalid                    | Medium             |
| FR03-TC-B02  | Email không tồn tại trong DB                                          | Đang ở B1                       | Nhập email không tồn tại & Submit                                                             | `email`=`notfound@eshop.com`                                                                                   | Hệ thống hiển thị thông báo "Tài khoản không tồn tại".                   | Invalid                    | High               |
| FR03-TC-B03  | Mã OTP nhập vào sai                                                   | Đã qua B1, đang ở B2            | Nhập OTP sai & Submit                                                                         | `resetToken`=`9999` (sai)                                                                                      | Hệ thống từ chối, báo lỗi mã OTP không đúng.                             | Invalid                    | High               |
| FR03-TC-B04  | Pass mới theo luật UI thực tế (Có khoảng trắng, không ký tự đặc biệt) | Đã qua B1, đang ở B2            | Nhập pass theo UI & Submit                                                                    | `newPassword`=`Password 123`                                                                                   | **Hệ thống báo lỗi** yêu cầu phải có ký tự đặc biệt theo chuẩn FR-01.    | Valid (theo UI)            | High               |
| FR03-TC-B05  | Pass mới chuẩn đặc tả nhưng UI từ chối                                | Đã qua B1, đang ở B2            | Nhập pass chuẩn đặc tả & Submit                                                               | `newPassword`=`Test@1234`                                                                                      | **Hệ thống chấp nhận**, đặt lại mật khẩu thành công.                     | Invalid (theo UI)          | High               |
| FR03-TC-B06  | Pass thiếu chữ hoa                                                    | Đang ở B2                       | Nhập pass & Submit                                                                            | `newPassword`=`test 1234`                                                                                      | Hệ thống từ chối, báo lỗi mật khẩu chưa đủ mạnh.                         | Invalid                    | Medium             |
| FR03-TC-B07  | Pass thiếu chữ thường                                                 | Đang ở B2                       | Nhập pass & Submit                                                                            | `newPassword`=`TEST 1234`                                                                                      | Hệ thống từ chối, báo lỗi mật khẩu chưa đủ mạnh.                         | Invalid                    | Medium             |
| FR03-TC-B08  | Pass thiếu số                                                         | Đang ở B2                       | Nhập pass & Submit                                                                            | `newPassword`=`Password ABC`                                                                                   | Hệ thống từ chối, báo lỗi mật khẩu chưa đủ mạnh.                         | Invalid                    | Medium             |
| FR03-TC-C01  | BVA: OTP length = 3                                                   | Đang ở B2                       | Nhập OTP 3 số                                                                                 | `resetToken`=`123`                                                                                             | Hệ thống báo lỗi mã OTP phải đủ 6 chữ số.                                | Invalid                    | Medium             |
| FR03-TC-C02  | BVA: OTP length = 4 (Biên UI)                                         | Đang ở B2                       | Nhập OTP 4 số                                                                                 | `resetToken`=`1234`                                                                                            | Hệ thống báo lỗi mã OTP phải đủ 6 chữ số (vì spec đòi 6).                | Valid (theo UI)            | High               |
| FR03-TC-C03  | BVA: OTP length = 5                                                   | Đang ở B2                       | Nhập OTP 5 số                                                                                 | `resetToken`=`12345`                                                                                           | Hệ thống báo lỗi mã OTP phải đủ 6 chữ số.                                | Invalid                    | Medium             |
| FR03-TC-C04  | BVA: Pass length = 7 (OFF)                                            | Đang ở B2                       | Nhập Pass 7 ký tự                                                                             | `newPassword`=`Pass 12`                                                                                        | Báo lỗi độ dài mật khẩu phải tối thiểu 8 ký tự.                          | Invalid                    | High               |
| FR03-TC-C05  | BVA: Pass length = 8 (ON)                                             | Đang ở B2                       | Nhập Pass 8 ký tự                                                                             | `newPassword`=`Pass 123`                                                                                       | (Thiếu ký tự đặc biệt) Báo lỗi định dạng mật khẩu.                       | Valid (theo UI)            | High               |
| FR03-TC-C06  | BVA: Pass length = 9                                                  | Đang ở B2                       | Nhập Pass 9 ký tự                                                                             | `newPassword`=`Pass 1234`                                                                                      | (Thiếu ký tự đặc biệt) Báo lỗi định dạng mật khẩu.                       | Valid (theo UI)            | Medium             |

---

## 4. Khung thực thi (Test EXECUTION Skeleton)

| Test Case ID | Kết quả thực tế (Actual) | Trạng thái (Pass/Fail/Blocked) | Ngày chạy | Người test | Môi trường/Build | Bug ID liên quan | Ghi chú nghi vấn (từ phân tích code)                                  |
| ------------ | ------------------------ | ------------------------------ | --------- | ---------- | ---------------- | ---------------- | --------------------------------------------------------------------- |
| FR03-TC-A01  |                          |                                |           |            |                  |                  | NGHI VẤN: Blocked do thiếu trường Confirm Pass và OTP chỉ có 4 số     |
| FR03-TC-B01  |                          |                                |           |            |                  |                  | NGHI VẤN: Web dùng `type="text"` nên HTML5 sẽ không validate          |
| FR03-TC-B02  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-B03  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-B04  |                          |                                |           |            |                  |                  | NGHI VẤN: Pass có khoảng trắng sẽ được hệ thống chấp nhận (Sai logic) |
| FR03-TC-B05  |                          |                                |           |            |                  |                  | NGHI VẤN: Pass chuẩn sẽ bị chặn lại do regex sai ở frontend           |
| FR03-TC-B06  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-B07  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-B08  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-C01  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-C02  |                          |                                |           |            |                  |                  | NGHI VẤN: Sẽ pass do backend chỉ sinh 4 số                            |
| FR03-TC-C03  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-C04  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-C05  |                          |                                |           |            |                  |                  |                                                                       |
| FR03-TC-C06  |                          |                                |           |            |                  |                  |                                                                       |

---

## 5. Báo cáo Lỗi (Defect / Bug Report) - Phân tích tĩnh (Static Analysis)

| Bug ID      | Tiêu đề (Title)                                                                 | Tiền điều kiện & Môi trường | Các bước tái hiện (đánh số)                                                  | Kết quả mong đợi                                  | Kết quả thực tế                                             | Severity | Priority | Trạng thái | Vị trí (File:Line)                        | Bằng chứng (ảnh/log)                   |
| ----------- | ------------------------------------------------------------------------------- | --------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------- | -------- | -------- | ---------- | ----------------------------------------- | -------------------------------------- |
| BUG-FR03-01 | **[Blocker] Thiếu trường Xác nhận mật khẩu mới**                                | Môi trường Web              | 1. Nhập email lấy OTP<br>2. Ở Bước 2 quan sát form nhập                      | Phải có trường "Xác nhận mật khẩu mới"            | Hoàn toàn không có trường này trên giao diện                | Critical | High     | Suspected  | `ForgotPassword.jsx:L63-L97`              | `![screenshot](./img/BUG-FR03-01.png)` |
| BUG-FR03-02 | **[Blocker] Regex mật khẩu bị sai (Cấm ký tự đặc biệt, bắt buộc khoảng trắng)** | Môi trường Web              | 1. Tới Bước 2<br>2. Nhập `Test@1234` vào Pass mới<br>3. Bấm Đặt lại mật khẩu | Đặt lại mật khẩu thành công                       | Báo lỗi mật khẩu yếu. (Nhập `Test 1234` thì lại thành công) | Critical | High     | Suspected  | `ForgotPassword.jsx:L26`                  | `![screenshot](./img/BUG-FR03-02.png)` |
| BUG-FR03-03 | Sinh OTP 4 số thay vì 6 số                                                      | Môi trường Web              | 1. Nhập email yêu cầu OTP<br>2. Xem kết quả trả về                           | Hệ thống phải sinh mã 6 số ngẫu nhiên             | Mã sinh ra và hiển thị là 4 số (`Math.random() * 9000`)     | High     | Medium   | Suspected  | `server.js:L72`, `ForgotPassword.jsx:L69` | `![screenshot](./img/BUG-FR03-03.png)` |
| BUG-FR03-04 | Không hiển thị Step Indicator (Chỉ báo bước)                                    | Môi trường Web              | 1. Vào trang Quên mật khẩu<br>2. Chuyển sang bước 2                          | Có text hiển thị "Bước 1 / 2", "Bước 2 / 2"       | Không có bất kỳ chỉ báo bước nào                            | Low      | Low      | Suspected  | `ForgotPassword.jsx:L45-L97`              | `![screenshot](./img/BUG-FR03-04.png)` |
| BUG-FR03-05 | Thiếu nút "Quay lại đăng nhập" ở Bước 1                                         | Môi trường Web              | 1. Vào trang Quên mật khẩu                                                   | Phải có nút/link quay về `/login`                 | Không có nút quay lại (Chỉ có ở Bước 2)                     | Medium   | Medium   | Suspected  | `ForgotPassword.jsx:L45-L61`              | `![screenshot](./img/BUG-FR03-05.png)` |
| BUG-FR03-06 | Thiếu validate Type Email & Dấu `*` trường bắt buộc                             | Môi trường Web              | 1. Vào trang Quên mật khẩu                                                   | Trường Email phải dùng `type="email"`, có dấu `*` | Trường dùng `type="text"`, không có dấu `*`                 | Medium   | Medium   | Suspected  | `ForgotPassword.jsx:L50`                  | `![screenshot](./img/BUG-FR03-06.png)` |
| BUG-FR03-07 | Dùng alert() thay vì render lỗi trên UI                                         | Môi trường Web              | 1. Gây lỗi ở Bước 1 hoặc Bước 2                                              | Báo lỗi xuất hiện trên nút Submit                 | Lỗi bật lên thành popup `alert()` của trình duyệt           | Medium   | Low      | Suspected  | `ForgotPassword.jsx:L20`, `L28`, `L37`    | `![screenshot](./img/BUG-FR03-07.png)` |
| BUG-FR03-08 | Sai màu nút Submit                                                              | Môi trường Web              | 1. Quan sát nút "Đặt lại mật khẩu" và "Quay lại"                             | Nút hành động phải dùng màu xanh dương            | Nút dùng class `bg-green-600` (Xanh lá)                     | Low      | Low      | Suspected  | `ForgotPassword.jsx:L90`, `L93`           | `![screenshot](./img/BUG-FR03-08.png)` |
| BUG-FR03-09 | Dùng sai thẻ H1                                                                 | Môi trường Web              | 1. Quan sát tiêu đề trang                                                    | Tiêu đề là thẻ `<h1>` duy nhất                    | Dùng thẻ `<h2>` làm tiêu đề chính                           | Low      | Low      | Suspected  | `ForgotPassword.jsx:L43`                  | `![screenshot](./img/BUG-FR03-09.png)` |
| BUG-FR03-10 | Lỗ hổng bảo mật: OTP không có thời hạn hết hạn                                  | Môi trường API              | 1. Tạo OTP<br>2. Chờ 1 ngày rồi dùng                                         | OTP phải hết hạn                                  | Backend lưu `reset_token` vĩnh viễn cho đến khi bị ghi đè   | High     | High     | Suspected  | `server.js:L87-L98`                       | `![screenshot](./img/BUG-FR03-10.png)` |

---

## 6. Tóm tắt Kiểm thử (Test Summary)

- **Thống kê Test Case:**
  - Thiết kế (Designed): 15
  - Đã chạy (Executed): (điền sau khi chạy)
  - Passed: (điền sau khi chạy)
  - Failed: (điền sau khi chạy)
  - Blocked: (điền sau khi chạy)

- **Thống kê Báo cáo lỗi (Suspected từ phân tích code tĩnh):**
  - **Critical:** 2 (Lỗi Regex pass, Thiếu trường Confirm)
  - **High:** 2 (Sinh sai số lượng OTP, OTP không hết hạn)
  - **Medium:** 3 (Thiếu nút Quay lại, Sai type email, Báo lỗi alert)
  - **Low:** 3 (Step Indicator, Màu nút, Thẻ HTML)
  - **Tổng cộng:** 10 Bugs

- **Đánh giá rủi ro & Khuyến nghị:**
  - **Rủi ro cực cao:** Chức năng bị tê liệt một nửa do người dùng không thể tạo mật khẩu đúng chuẩn (bị Regex chặn) và thiếu trường Xác nhận Mật khẩu. Các lỗi về UX (dùng alert, màu sai) làm giảm trải nghiệm đáng kể.
  - **Bảo mật:** Việc OTP sinh ra chỉ có 4 số và **không có hàm kiểm tra thời hạn hết hạn** trong CSDL (cột `reset_token` không đi kèm `reset_token_expiry`) tạo ra lỗ hổng bảo mật nghiêm trọng (SEC-07).
  - **Khuyến nghị sửa ngay:**
    1. Sửa regex tại `ForgotPassword.jsx:L26` thành: `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/`
    2. Thêm input cho "Xác nhận mật khẩu".
    3. Thêm cột `reset_token_expiry` ở backend và validate thời hạn tại `server.js:L90`.

---

### Phụ lục A — Inconsistency đặc tả (readme) vs UI thật

| Biến              | Readme yêu cầu               | UI thật thực hiện                         | Ảnh hưởng tới test                                                              | Ghi chú/Finding                  |
| ----------------- | ---------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------- |
| `email`           | `type="email"`, có dấu `*`   | `type="text"`, không có dấu `*`           | Test case nhập sai định dạng có thể bị Backend bắt thay vì HTML5 bắt ở Frontend | Ghi nhận BUG Medium.             |
| `resetToken`      | OTP 6 chữ số ngẫu nhiên      | Sinh và yêu cầu nhập 4 chữ số             | Test case phải bám theo 4 số của UI để test                                     | Ghi nhận BUG High.               |
| `newPassword`     | Có ký tự đặc biệt, >=8 ký tự | Bắt buộc khoảng trắng, cấm ký tự đặc biệt | Pass chuẩn bị từ chối, pass sai thành công                                      | Blocker BUG cực kỳ nghiêm trọng. |
| `confirmPassword` | Bắt buộc phải có và khớp     | Hoàn toàn biến mất khỏi form              | Không thể thiết kế test case cho hành vi này qua UI                             | Blocker BUG.                     |
| Step Indicator    | Có hiển thị "Bước 1 / 2"     | Không có bất kỳ text nào                  | Giao diện bị thiếu chức năng điều hướng                                         | Ghi nhận BUG.                    |

### Phụ lục B — Reserved cho bài API Testing

_(Không có test case nào gọi thẳng API bypass UI trong bảng chính, chức năng này hoàn toàn test thông qua tương tác người dùng trên giao diện Web.)_
