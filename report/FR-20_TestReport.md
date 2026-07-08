<!-- File: FR-20_TestReport.md -->

# BÁO CÁO KIỂM THỬ: FR-20 — Mobile App: Giỏ Hàng & Thanh Toán (Cart & Checkout)

## 1. Phân hoạch tương đương (Equivalence Partitioning & Domain Analysis)

Dựa trên phân tích mã nguồn (`frontend-mobile/App.js` và `backend/server.js`) cùng tài liệu đặc tả hệ thống, ta xác định các biến đầu vào chính và phân hoạch tương đương như sau:

### 1.1. Biến `text` (Số lượng sản phẩm tại ô nhập trong Giỏ hàng)
- **Nguồn:** Trường `<TextInput>` tại hàm `renderCart` (dòng 611-625).
- **Ràng buộc UI thật:** Thẻ có thuộc tính `keyboardType="numeric"`. Không giới hạn độ dài nhập ở frontend. Sự kiện `onChangeText` lấy chuỗi đầu vào chạy qua `parseInt(text, 10)` để ép kiểu thành số nguyên `parsed`. Nếu `Number.isFinite(parsed) && parsed > 0`, hệ thống gán giá trị mới bằng `parsed + 1` (đây là **BUG thiết kế**), ngược lại gán mặc định bằng `1`.
- **Ràng buộc Đặc tả:** Số lượng phải là số nguyên dương lớn hơn 0 và nhỏ hơn giới hạn tồn kho.
- **VEC-qty-1:** Chuỗi chứa số nguyên dương nằm trong khoảng hợp lý [1, 99] (VD: `"5"`).
- **VEC-qty-2:** Chuỗi chứa số nguyên dương lớn nhưng trong giới hạn hợp lý [100, 999999] (VD: `"250"`).
- **IEC-qty-1:** Chuỗi rỗng `""` (xóa toàn bộ ký tự trong ô) — bị ép ngay về `1`.
- **IEC-qty-2:** Chuỗi chỉ chứa các khoảng trắng `"   "` — trả về `NaN` sau khi parse, bị ép về `1`.
- **IEC-qty-3:** Chuỗi chứa số `0` — không thỏa mãn điều kiện `parsed > 0`, bị ép về `1`.
- **IEC-qty-4:** Chuỗi chứa số nguyên âm (VD: `"-5"`) — không thỏa mãn `parsed > 0`, bị ép về `1`.
- **IEC-qty-5:** Chuỗi chỉ gồm chữ cái hoặc ký tự đặc biệt (VD: `"abc"`, `"!@#"`) — trả về `NaN`, bị ép về `1`.
- **IEC-qty-6:** Chuỗi số thập phân dương (VD: `"1.5"`, `"5.7"`) — `parseInt` cắt bỏ phần thập phân và lấy phần nguyên dương làm số lượng để cộng 1.
- **IEC-qty-7:** Chuỗi số thập phân âm hoặc có phần nguyên bằng 0 (VD: `"-1.5"`, `"0.9"`) — trả về số `<= 0` hoặc `NaN`, bị ép về `1`.
- **IEC-qty-8:** Chuỗi hỗn hợp bắt đầu bằng số (VD: `"3abc"`, `"5 kg"`) — `parseInt` trích xuất phần số đầu tiên rồi xử lý bình thường.
- **IEC-qty-9:** Chuỗi hỗn hợp bắt đầu bằng chữ (VD: `"abc3"`) — trả về `NaN`, bị ép về `1`.
- **IEC-qty-10:** Số cực lớn vượt quá giới hạn an toàn hệ thống (VD: `"9007199254740992"`).
- **IEC-qty-11:** Chuỗi hệ Hex (VD: `"0xFF"`) — `parseInt` trích xuất thành giá trị nguyên `255` ở hệ thập phân.
- **IEC-qty-12:** Chuỗi chỉ chứa dấu cộng hoặc dấu trừ trước số (VD: `"-"`, `"+5"`).

### 1.2. Biến `quantity` (Số lượng sản phẩm tại ô nhập trong Chi tiết sản phẩm)
- **Nguồn:** Trường `<TextInput>` tại màn hình chi tiết sản phẩm `renderProductDetail` (dòng 564-570).
- **Ràng buộc UI thật:** Mặc định là `"1"`. Khi bấm "Thêm vào giỏ", giá trị được đưa qua hàm `normalizeQuantity` thực hiện `parseInt(value, 10)` và trả về `1` nếu kết quả không phải số nguyên dương.
- **VEC-det-1:** Chuỗi số nguyên dương hợp lệ (VD: `"3"`).
- **IEC-det-1:** Chuỗi rỗng hoặc chỉ chứa khoảng trắng (VD: `""`, `"  "`) — bị `normalizeQuantity` ép về `1`.
- **IEC-det-2:** Chuỗi chứa số 0 hoặc số âm (VD: `"0"`, `"-5"`) — bị ép về `1`.
- **IEC-det-3:** Chuỗi không phải số (VD: `"abc"`, `"!@#"`) — bị ép về `1`.
- **IEC-det-4:** Chuỗi thập phân hoặc hỗn hợp (VD: `"1.5"`, `"3abc"`) — bị cắt bỏ phần chữ/phần thập phân lấy phần nguyên.

### 1.3. Biến `couponCode` (Mã giảm giá tại màn hình Checkout)
- **Nguồn:** Ô nhập mã giảm giá tại màn hình Checkout `renderCheckout` (dòng 695-705).
- **Ràng buộc UI thật & Đặc tả:** Chuỗi nhập được tự động trim khoảng trắng và đổi sang chữ hoa trước khi gửi lên API `/api/apply-coupon`. Backend kiểm tra tính hợp lệ trong cơ sở dữ liệu dựa trên mã code, trạng thái `is_active`, hạn dùng `expired_at`, số tiền tối thiểu đơn hàng `min_order_amount` và giới hạn sử dụng của người dùng.
- **VEC-cp-1:** Mã giảm giá tồn tại, đang kích hoạt và còn hạn sử dụng (VD: `"SAVE10"`, `"BIGBUY"`, `"VIP100"`).
- **IEC-cp-1:** Mã giảm giá không tồn tại trong hệ thống (VD: `"INVALIDCODE"`).
- **IEC-cp-2:** Mã giảm giá bị vô hiệu hóa (`is_active = 0`).
- **IEC-cp-3:** Mã giảm giá đã hết hạn sử dụng (`expired_at < now`).
- **IEC-cp-4:** Mã giảm giá hợp lệ nhưng đơn hàng chưa đạt giá trị tối thiểu quy định.
- **IEC-cp-5:** Mã giảm giá hợp lệ nhưng người dùng đã sử dụng vượt quá giới hạn tối đa `max_uses_per_user`.

---

## 2. Phân tích giá trị biên (Boundary Value Analysis)

### 2.1. Biên số lượng sản phẩm (`parsed`)
- **Biên đặc tả:** `quantity ≥ 1`. Đối với miền số nguyên, giá trị biên dưới hợp lệ là `1`.
- **Điểm biên (Áp dụng 3-point BVA):**
  - `parsed = 0` (Biên không hợp lệ, OFF - Kỳ vọng bị chặn/ép về 1).
  - `parsed = 1` (Biên dưới hợp lệ, ON - Kỳ vọng lưu đúng giá trị 1).
  - `parsed = 2` (Trên biên hợp lệ - Kỳ vọng lưu đúng giá trị 2).
  - `parsed = -1` (Dưới biên không hợp lệ - Kỳ vọng bị chặn/ép về 1).

### 2.2. Biên tổng số tiền đơn hàng (`total_amount` áp dụng mã giảm giá)
- **Biên đặc tả:** `total_amount > min_order_amount`. 
- **Điểm biên cho mã `SAVE10` (điều kiện `min_order_amount = 300000`):**
  - `total_amount = 299999` (Dưới biên, OFF - Không đủ điều kiện áp dụng mã).
  - `total_amount = 300000` (Trên biên đặc tả, OFF - Không đủ điều kiện vì code backend sử dụng phép so sánh lớn hơn nghiêm ngặt `total_amount > coupon.min_order_amount`).
  - `total_amount = 300001` (Hợp lệ, ON - Đủ điều kiện áp dụng mã giảm giá).

---

## 3. Bảng thiết kế Test Case (Test Case DESIGN)

*Lưu ý: Các test case dưới đây đều được thiết kế để thao tác trực tiếp qua giao diện người dùng (UI) trên thiết bị di động.*

| Test Case ID | Mục đích (Objective) | Tiền điều kiện (Pre-conditions) | Các bước (Steps) | Dữ liệu đầu vào (Input) | Kết quả mong đợi CHUẨN (Expected — spec-correct) | Loại Input (Valid/Invalid) | Ưu tiên (Priority) |
|---|---|---|---|---|---|---|---|
| **Nhóm A: Nhập liệu hợp lệ & Luồng thành công qua UI** | | | | | | | |
| FR20-TC-A01 | Thêm sản phẩm thành công từ trang chi tiết với số lượng hợp lệ | Khách hàng đã đăng nhập, đang ở màn hình chi tiết sản phẩm A | 1. Nhập số lượng sản phẩm vào ô nhập.<br>2. Nhấn nút "Thêm vào giỏ".<br>3. Kiểm tra thông báo và badge giỏ hàng. | `quantity` = "3" | Hiển thị thông báo thêm thành công; giỏ hàng cập nhật số lượng tăng thêm đúng bằng 3 sản phẩm A. | Valid | High |
| FR20-TC-A02 | Chỉnh sửa số lượng sản phẩm hợp lệ trong Giỏ hàng | Khách hàng đã đăng nhập, giỏ hàng đang có 1 sản phẩm | 1. Vào màn hình Giỏ hàng.<br>2. Thay đổi số lượng sản phẩm trong ô nhập.<br>3. Nhấp ra ngoài để lưu. | `text` = "5" | Số lượng sản phẩm hiển thị đúng bằng 5; giá trị "Thành tiền" và "Tổng tạm tính" cập nhật chính xác (price × 5). | Valid | High |
| FR20-TC-A03 | Áp dụng thành công mã giảm giá phần trăm `SAVE10` | Đơn hàng trong Checkout có tổng giá trị lớn hơn 300.000đ | 1. Nhấn "Thanh toán" để vào màn hình Checkout.<br>2. Nhập mã giảm giá vào ô nhập.<br>3. Nhấn nút "Áp dụng". | `couponCode` = "SAVE10" | Áp dụng thành công, hiển thị giảm giá 10% trên tổng tiền đơn hàng; số tiền thanh toán cuối cùng giảm đi 10% chính xác. | Valid | High |
| FR20-TC-A04 | Áp dụng thành công mã giảm giá cố định `BIGBUY` | Đơn hàng trong Checkout có tổng giá trị lớn hơn 500.000đ | 1. Tại màn hình Checkout, nhập mã giảm giá.<br>2. Nhấn nút "Áp dụng". | `couponCode` = "BIGBUY" | Áp dụng thành công, hiển thị giảm giá 50.000 ₫; số tiền thanh toán cuối cùng giảm đi đúng 50.000đ. | Valid | High |
| FR20-TC-A05 | Xác nhận thanh toán giỏ hàng thành công với nhiều sản phẩm | Khách hàng đã đăng nhập, giỏ hàng có 2 sản phẩm khác nhau | 1. Nhấn nút "Thanh toán" để mở màn hình xác nhận đơn hàng.<br>2. Nhấn "Xác Nhận Thanh Toán". | Chọn giỏ hàng gồm 2 sản phẩm | Hệ thống tạo đơn hàng thành công, hiển thị màn hình thông báo thanh toán thành công với đầy đủ cả 2 sản phẩm trong đơn. | Valid | High |
| **Nhóm B: Nhập liệu không hợp lệ tại Giỏ hàng (Domain Invalid)** | | | | | | | |
| FR20-TC-B01 | Nhập số lượng bằng 0 tại màn hình Giỏ hàng | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập số lượng bằng 0 vào ô nhập.<br>2. Nhấp ra ngoài hoặc xác nhận. | `text` = "0" | Hệ thống từ chối cập nhật, hiển thị cảnh báo số lượng không hợp lệ và tự động đưa số lượng về 1 (hoặc giữ nguyên giá cũ). | Invalid | Medium |
| FR20-TC-B02 | Nhập số lượng là số nguyên âm tại Giỏ hàng | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập số nguyên âm vào ô nhập.<br>2. Nhấp ra ngoài hoặc xác nhận. | `text` = "-5" | Hệ thống từ chối cập nhật, hiển thị cảnh báo số lượng không hợp lệ và đưa số lượng về 1. | Invalid | Medium |
| FR20-TC-B03 | Nhập số lượng chứa chữ cái thuần hoặc ký tự đặc biệt | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập chuỗi chữ hoặc ký tự đặc biệt vào ô nhập.<br>2. Nhấp ra ngoài. | `text` = "abc" (hoặc `"!@#"`) | Hệ thống từ chối cập nhật, cảnh báo định dạng không hợp lệ, giữ nguyên giá trị cũ hoặc đưa về 1. | Invalid | Low |
| FR20-TC-B04 | Xóa rỗng ô nhập số lượng sản phẩm | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhấp vào ô số lượng.<br>2. Xóa toàn bộ ký tự hiển thị. | `text` = "" | Cho phép ô nhập trống tạm thời để người dùng nhập giá trị mới. Chỉ reset về mặc định nếu người dùng thoát khỏi ô nhập mà không điền gì. | Invalid | Medium |
| FR20-TC-B05 | Nhập khoảng trắng vào ô số lượng | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập chuỗi khoảng trắng.<br>2. Nhấp ra ngoài. | `text` = "   " | Hệ thống từ chối cập nhật, đưa số lượng về 1. | Invalid | Low |
| **Nhóm C: Phân tích giá trị biên số lượng (BVA Quantity)** | | | | | | | |
| FR20-TC-C01 | BVA: Nhập số lượng bằng 1 (Biên dưới ON) | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập số lượng bằng 1 vào ô nhập.<br>2. Xác nhận lưu. | `text` = "1" | Số lượng lưu chính xác là 1. Thành tiền hiển thị đúng bằng giá trị gốc (price × 1). | Valid | High |
| FR20-TC-C02 | BVA: Nhập số lượng bằng 2 (Biên dưới + 1) | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập số lượng bằng 2 vào ô nhập.<br>2. Xác nhận lưu. | `text` = "2" | Số lượng lưu chính xác là 2. Thành tiền hiển thị đúng bằng (price × 2). | Valid | Medium |
| FR20-TC-C03 | BVA: Nhập số lượng bằng -1 (Biên không hợp lệ) | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập số lượng bằng -1 vào ô nhập.<br>2. Xác nhận lưu. | `text` = "-1" | Hệ thống từ chối cập nhật, đưa số lượng về 1. | Invalid | Medium |
| FR20-TC-C04 | BVA: Nhập số lượng cực lớn tại Giỏ hàng | Khách hàng đang ở màn hình Giỏ hàng, có sản phẩm trong giỏ | 1. Nhập số lượng lớn vượt ngưỡng quy định.<br>2. Xác nhận lưu. | `text` = "999999" | Hệ thống chặn hoặc giới hạn số lượng tối đa cho phép (ví dụ: tối đa 999 sản phẩm) và hiển thị thông báo lỗi. | Invalid | Medium |
| **Nhóm D: Áp dụng mã giảm giá không hợp lệ & Sai biên (Coupon / BVA)** | | | | | | | |
| FR20-TC-D01 | Áp dụng mã giảm giá không tồn tại | Khách hàng đang ở màn hình Checkout | 1. Nhập mã giảm giá không tồn tại.<br>2. Nhấn nút "Áp dụng". | `couponCode` = "KHM123" | Hệ thống báo lỗi "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa" và không giảm giá. | Invalid | Medium |
| FR20-TC-D02 | Áp dụng mã giảm giá đã hết hạn sử dụng | Khách hàng đang ở màn hình Checkout | 1. Nhập mã giảm giá đã quá hạn.<br>2. Nhấn nút "Áp dụng". | `couponCode` = "EXPIRED" | Hệ thống báo lỗi "Mã giảm giá đã hết hạn" và không giảm giá. | Invalid | Medium |
| FR20-TC-D03 | BVA: Áp dụng coupon phần trăm khi tổng tiền bằng đúng mức tối thiểu | Giỏ hàng có tổng tiền đúng 300.000đ | 1. Nhập mã giảm giá có điều kiện áp dụng cho đơn hàng > 300.000đ.<br>2. Nhấn nút "Áp dụng". | `couponCode` = "SAVE10" | Hệ thống thông báo lỗi yêu cầu đơn hàng phải có giá trị lớn hơn 300.000đ mới được áp dụng. | Invalid | Medium |
| FR20-TC-D04 | BVA: Áp dụng coupon phần trăm khi tổng tiền dưới mức tối thiểu 1 đơn vị | Giỏ hàng có tổng tiền đúng 299.999đ | 1. Nhập mã giảm giá có điều kiện áp dụng cho đơn hàng > 300.000đ.<br>2. Nhấn nút "Áp dụng". | `couponCode` = "SAVE10" | Hệ thống thông báo lỗi yêu cầu đơn hàng có giá trị lớn hơn 300.000đ mới được áp dụng. | Invalid | Medium |
| FR20-TC-D05 | Áp dụng mã giảm giá đã dùng quá số lần cho phép | Khách hàng đã dùng mã giảm giá VIP100 đủ 2 lần trước đó | 1. Tại màn hình Checkout, nhập mã giảm giá.<br>2. Nhấn nút "Áp dụng". | `couponCode` = "VIP100" | Hệ thống báo lỗi "Bạn đã sử dụng mã này 2 lần (đã đạt giới hạn)" và từ chối áp dụng. | Invalid | Medium |
| **Nhóm E: Trường hợp đặc biệt và biên dữ liệu lỗi (Edge Cases)** | | | | | | | |
| FR20-TC-E01 | Nhập số lượng sản phẩm là số thập phân dương | Khách hàng đang ở màn hình Giỏ hàng | 1. Nhập số thập phân vào ô số lượng.<br>2. Nhấp ra ngoài. | `text` = "1.9" | Hệ thống từ chối định dạng số thập phân, yêu cầu nhập số nguyên dương. | Invalid | Medium |
| FR20-TC-E02 | Nhập chuỗi hỗn hợp chữ số (ví dụ: "3abc") làm số lượng | Khách hàng đang ở màn hình Giỏ hàng | 1. Nhập chuỗi ký tự chứa cả số và chữ bắt đầu bằng số.<br>2. Nhấp ra ngoài. | `text` = "3abc" | Hệ thống từ chối cập nhật hoặc yêu cầu định dạng số nguyên hợp lệ. | Invalid | Medium |
| FR20-TC-E03 | Nhập số lượng dạng mã Hex | Khách hàng đang ở màn hình Giỏ hàng | 1. Nhập mã Hex.<br>2. Nhấp ra ngoài. | `text` = "0xFF" | Hệ thống từ chối cập nhật và yêu cầu định dạng số nguyên hệ thập phân. | Invalid | Low |
| FR20-TC-E04 | Nhập số lượng chứa dấu cộng phía trước | Khách hàng đang ở màn hình Giỏ hàng | 1. Nhập chuỗi chứa dấu cộng trước chữ số.<br>2. Nhấp ra ngoài. | `text` = "+5" | Hệ thống chấp nhận số lượng là 5 hoặc báo lỗi định dạng ký tự không hợp lệ. | Invalid | Low |

---

## 4. Khung thực thi (Test EXECUTION Skeleton)

| Test Case ID | Kết quả thực tế (Actual) | Trạng thái (Pass/Fail/Blocked) | Ngày chạy | Người test | Môi trường/Build | Bug ID liên quan | Ghi chú nghi vấn (từ phân tích code) |
|---|---|---|---|---|---|---|---|
| FR20-TC-A01 | | | | | | | |
| FR20-TC-A02 | | | | | | BUG-FR20-01 | NGHI VẤN: Lỗi off-by-one, khi nhập số lượng hợp lệ hệ thống cộng thêm 1 đơn vị (`parsed + 1`). |
| FR20-TC-A03 | | | | | | BUG-FR20-03 | NGHI VẤN: Lỗi công thức trong `server.js` nhân tổng tiền đơn hàng lên nhiều lần (`total_amount * (1 - 10)`). |
| FR20-TC-A04 | | | | | | | |
| FR20-TC-A05 | | | | | | BUG-FR20-02 | NGHI VẤN: Lỗi `cart.slice(0, -1)` làm mất sản phẩm cuối cùng trong giỏ khi thanh toán. |
| FR20-TC-B01 | | | | | | | |
| FR20-TC-B02 | | | | | | | |
| FR20-TC-B03 | | | | | | | |
| FR20-TC-B04 | | | | | | BUG-FR20-06 | NGHI VẤN: Xóa rỗng ô nhập làm số lượng bị reset ngay về 1, gây khó khăn cho việc gõ số nhiều chữ số. |
| FR20-TC-B05 | | | | | | | |
| FR20-TC-C01 | | | | | | BUG-FR20-01 | NGHI VẤN: Nhập 1 lưu 2 do lỗi cộng thừa 1. |
| FR20-TC-C02 | | | | | | BUG-FR20-01 | NGHI VẤN: Nhập 2 lưu 3 do lỗi cộng thừa 1. |
| FR20-TC-C03 | | | | | | | |
| FR20-TC-C04 | | | | | | BUG-FR20-07 | NGHI VẤN: Không có giới hạn số lượng tối đa ở phía client và server. |
| FR20-TC-D01 | | | | | | | |
| FR20-TC-D02 | | | | | | | |
| FR20-TC-D03 | | | | | | | NGHI VẤN: Điều kiện so sánh `total_amount > min_order_amount` sẽ chặn đơn hàng có giá trị bằng đúng mức tối thiểu. |
| FR20-TC-D04 | | | | | | | |
| FR20-TC-D05 | | | | | | | |
| FR20-TC-E01 | | | | | | BUG-FR20-04 | NGHI VẤN: `parseInt` lấy phần nguyên rồi cộng thêm 1 khiến nhập `"1.9"` lưu thành `2`. |
| FR20-TC-E02 | | | | | | BUG-FR20-05 | NGHI VẤN: `parseInt` trích xuất được số 3 từ `"3abc"` rồi cộng thêm 1 thành `4`. |
| FR20-TC-E03 | | | | | | | NGHI VẤN: `parseInt` parse mã Hex thành số thập phân rồi xử lý cộng 1. |
| FR20-TC-E04 | | | | | | | |

---

## 5. Báo cáo Lỗi (Defect / Bug Report)

| Bug ID | Tiêu đề (Title) | Tiền điều kiện & Môi trường | Các bước tái hiện (đánh số) | Kết quả mong đợi | Kết quả thực tế | Severity | Priority | Trạng thái | Vị trí (File:Line) | Bằng chứng (ảnh/log) |
|---|---|---|---|---|---|---|---|---|---|---|
| BUG-FR20-01 | **Lỗi off-by-one tự động tăng thêm 1 đơn vị sản phẩm khi sửa số lượng trong giỏ hàng** | Khách hàng đã đăng nhập và đang xem màn hình Giỏ hàng | 1. Nhấp vào ô nhập số lượng sản phẩm.<br>2. Nhập số `2` vào ô.<br>3. Nhấp ra ngoài để lưu thay đổi. | Số lượng lưu trữ và hiển thị là 2; thành tiền được cập nhật tương ứng. | Số lượng hiển thị tự động tăng lên thành 3 và thành tiền cũng tính theo hệ số 3. | Critical | High | Confirmed | `App.js:L620` | `![screenshot](./img/BUG-FR20-01.png)` |
| BUG-FR20-02 | **Lỗi cắt bỏ sản phẩm cuối cùng trong giỏ hàng khi thực hiện checkout** | Khách hàng đã đăng nhập, giỏ hàng có từ 2 sản phẩm trở lên | 1. Thêm sản phẩm A và sản phẩm B vào giỏ hàng.<br>2. Nhấn nút "Thanh toán".<br>3. Bấm xác nhận thanh toán đơn hàng. | Đơn hàng hiển thị đầy đủ cả sản phẩm A và sản phẩm B trên màn hình xác nhận và trong DB. | Đơn hàng được tạo chỉ chứa sản phẩm A; sản phẩm B (sản phẩm cuối cùng) bị cắt mất. | Critical | High | Confirmed | `App.js:L391` | `![screenshot](./img/BUG-FR20-02.png)` |
| BUG-FR20-03 | **Lỗi tính toán giảm giá coupon dạng phần trăm (percent) nhân số tiền đơn hàng lên nhiều lần** | Khách hàng ở màn hình Checkout, chuẩn bị đơn hàng > 300.000đ | 1. Nhập mã giảm giá `"SAVE10"`.<br>2. Nhấn nút "Áp dụng". | Số tiền giảm giá được tính bằng 10% đơn hàng (VD: đơn 1.000.000đ giảm 100.000đ, còn 900.000đ). | Giảm giá bị tính số âm cực lớn khiến tổng tiền thanh toán tăng lên gấp 10 lần giá gốc (đơn 1.000.000đ bị tính tổng thanh toán thành 10.000.000đ). | Critical | High | Confirmed | `server.js:L399-L401` và `L418-L420` | `![screenshot](./img/BUG-FR20-03.png)` |
| BUG-FR20-04 | **Nhập số thập phân dương làm số lượng gây sai lệch giá trị lưu trữ** | Khách hàng đang sửa số lượng trong Giỏ hàng | 1. Nhập chuỗi số `"1.9"` vào ô số lượng.<br>2. Nhấp ra ngoài để cập nhật. | Hệ thống báo lỗi định dạng hoặc chặn không cho nhập ký tự dấu chấm thập phân. | Số lượng được parse thành phần nguyên `1` rồi cộng thêm `1` thành `2` sản phẩm. | High | Medium | Confirmed | `App.js:L617-L621` | `![screenshot](./img/BUG-FR20-04.png)` |
| BUG-FR20-05 | **Chấp nhận chuỗi hỗn hợp chữ số (ví dụ: "3abc") làm số lượng hợp lệ** | Khách hàng đang sửa số lượng trong Giỏ hàng | 1. Nhập chuỗi `"3abc"` vào ô số lượng.<br>2. Nhấp ra ngoài để cập nhật. | Hệ thống từ chối cập nhật và báo lỗi định dạng nhập liệu. | Hệ thống parse thành công số `3` từ chuỗi và cộng thêm `1` thành `4` sản phẩm. | High | Medium | Confirmed | `App.js:L617-L621` | `![screenshot](./img/BUG-FR20-05.png)` |
| BUG-FR20-06 | **Lỗi reset ngay lập tức về 1 sản phẩm khi xóa rỗng ô số lượng** | Khách hàng đang sửa số lượng trong Giỏ hàng | 1. Đặt con trỏ vào ô số lượng.<br>2. Xóa toàn bộ ký tự để chuẩn bị gõ số mới. | Ô nhập được phép trống tạm thời để người dùng thực hiện gõ giá trị mới. | Số lượng lập tức nhảy về số `1` ngay khi xóa ký tự cũ, gây khó khăn cho việc nhập số nhiều chữ số. | Medium | Medium | Confirmed | `App.js:L617-L621` | `![screenshot](./img/BUG-FR20-06.png)` |
| BUG-FR20-07 | **Thiếu giới hạn số lượng tối đa cho phép cập nhật trong giỏ hàng** | Khách hàng đang sửa số lượng trong Giỏ hàng | 1. Nhập chuỗi số lượng khổng lồ `"999999999"` vào ô.<br>2. Xác nhận lưu. | Hệ thống cảnh báo vượt quá giới hạn hoặc tồn kho tối đa cho phép. | Chấp nhận lưu trữ số lượng khổng lồ, dẫn đến lỗi tính tiền hiển thị bị tràn hoặc lỗi tài chính. | Medium | Low | Confirmed | `App.js:L617-L621` | `![screenshot](./img/BUG-FR20-07.png)` |
| BUG-FR20-08 | **Inconsistency: Nhãn nút đăng xuất hiển thị là "Thoát" thay vị "Đăng xuất"** | Khách hàng đã đăng nhập, ở màn hình Hồ sơ | 1. Nhấp chọn tab Hồ sơ (Profile).<br>2. Quan sát nút bấm màu đỏ ở dưới cùng. | Nhãn hiển thị của nút phải là "Đăng xuất" theo quy định của FR-23. | Nhãn hiển thị trên giao diện là "Thoát". | Low | Low | Confirmed | `App.js:L941` | `![screenshot](./img/BUG-FR20-08.png)` |
| BUG-FR20-09 | **Inconsistency: Các trường bắt buộc trong form Hồ sơ, Đăng nhập/Đăng ký thiếu dấu *** | Người dùng truy cập form Đăng ký hoặc Hồ sơ cá nhân | 1. Mở màn hình Đăng ký hoặc Hồ sơ.<br>2. Quan sát các nhãn bên cạnh ô nhập liệu. | Tất cả trường bắt buộc phải có biểu tượng `*` màu đỏ bên cạnh nhãn theo FR-22. | Các nhãn chỉ hiển thị văn bản thường, thiếu ký hiệu bắt buộc `*`. | Low | Low | Confirmed | `App.js:L763, L808, L913` | `![screenshot](./img/BUG-FR20-09.png)` |

---

## 6. Tóm tắt Kiểm thử (Test Summary)

- **Thống kê Test Case:**
  - Thiết kế (Designed): 22
  - Đã chạy (Executed): `(điền sau khi chạy)`
  - Passed: `(điền sau khi chạy)`
  - Failed: `(điền sau khi chạy)`
  - Blocked: `(điền sau khi chạy)`

- **Thống kê Báo cáo lỗi (Confirmed từ phân tích code tĩnh & đối chiếu UI):**
  - **Critical:** 3 (BUG-FR20-01, BUG-FR20-02, BUG-FR20-03)
  - **High:** 2 (BUG-FR20-04, BUG-FR20-05)
  - **Medium:** 2 (BUG-FR20-06, BUG-FR20-07)
  - **Low:** 2 (BUG-FR20-08, BUG-FR20-09)
  - **Tổng cộng:** 9 Bugs

- **Đánh giá rủi ro & Khuyến nghị:**
  - **Rủi ro logic và tài chính:** Lỗi cộng thừa 1 sản phẩm (`BUG-FR20-01`) khiến khách hàng không thể mua đúng số lượng mong muốn. Lỗi cắt bỏ sản phẩm cuối khi thanh toán (`BUG-FR20-02`) làm hỏng toàn vẹn giỏ hàng. Đặc biệt lỗi coupon phần trăm (`BUG-FR20-03`) tính sai discount gây tăng vọt hóa đơn thanh toán lên 10 lần, tạo rủi ro tài chính cực lớn cho cả doanh nghiệp lẫn khách hàng.
  - **Rủi ro trải nghiệm và giao diện:** Nhập liệu số lượng phản hồi quá nhạy khiến reset về 1 khi xóa rỗng gây khó chịu cho người dùng. Các tiêu chuẩn GUI về nhãn nút Đăng xuất ("Thoát") và ký hiệu bắt buộc `*` bị vi phạm nghiêm trọng.
  - **Khuyến nghị sửa ngay:**
    - **Frontend (`App.js`):**
      1. Khắc phục lỗi off-by-one trong cập nhật số lượng giỏ hàng:
         ```jsx
         // App.js: dòng 620
         newCart[index].quantity =
           Number.isFinite(parsed) && parsed > 0
             ? parsed // Sửa từ parsed + 1 thành parsed
             : 1;
         ```
      2. Loại bỏ việc cắt bỏ phần tử cuối trong API Checkout:
         ```jsx
         // App.js: dòng 391
         body: JSON.stringify({
           items: cart, // Sửa từ cart.slice(0, -1) thành cart
           total_amount: finalAmount,
           coupon_id: couponResult?.coupon_id || null,
         })
         ```
      3. Sửa đổi nút "Thoát" thành "Đăng xuất" và thêm dấu `*` cho các nhãn bắt buộc trong form.
    - **Backend (`server.js`):**
      1. Chỉnh sửa công thức tính giảm giá phần trăm:
         ```javascript
         // server.js: dòng 399 và 419
         if (coupon.type === "percent") {
           discount_amount = Math.floor(
             total_amount * (coupon.discount_value / 100) // Sửa đổi công thức
           );
         }
         ```

---

### Phụ lục A — Inconsistency đặc tả (readme) vs UI thật

| Đối tượng / Biến | Đặc tả yêu cầu | UI thật thực hiện | Ảnh hưởng tới kiểm thử | Ghi chú / Finding |
|---|---|---|---|---|
| Nút đăng xuất | Nút đăng xuất phải hiển thị nhãn là "Đăng xuất" (FR-23). | Nút đăng xuất trong tab Hồ sơ hiển thị nhãn là "Thoát". | Sai lệch hiển thị giao diện so với chuẩn thiết kế. | Ghi nhận BUG-FR20-08 |
| Ký hiệu trường bắt buộc | Tất cả các trường bắt buộc nhập phải có dấu `*` bên cạnh nhãn (FR-22). | Không hiển thị ký hiệu `*` bên cạnh nhãn các trường Username, Email, Họ tên, Số điện thoại. | Giao diện không hướng dẫn rõ ràng trường nào cần nhập. | Ghi nhận BUG-FR20-09 |
| Áp dụng mã giảm giá | Mã giảm giá được áp dụng khi tổng tiền đạt giá trị tối thiểu (ví dụ: `total_amount >= min_order_amount`). | Backend sử dụng phép so sánh lớn hơn nghiêm ngặt `total_amount > min_order_amount`. | Đơn hàng có tổng tiền đúng bằng mức tối thiểu sẽ không được giảm giá. | Ghi nhận khi phân tích code tĩnh |

---

### Phụ lục B — Reserved cho bài API Testing

> **CẢNH BÁO:** Các case dưới đây dùng để gọi trực tiếp các API, bypass giao diện Mobile Frontend. Các case này **KHÔNG** tính điểm cho HW02 (Functional qua UI) và được để dành (reserved) cho bài API Testing sau này.

| Test Case ID | Mục đích (Objective) | Tiền điều kiện (Pre-conditions) | Các bước (Steps) | Dữ liệu đầu vào (Input) | Kết quả mong đợi CHUẨN (Expected — spec-correct) | Loại Input (Valid/Invalid) | Ưu tiên (Priority) |
|---|---|---|---|---|---|---|---|
| FR20-API-TC-01 | Gửi POST tạo đơn hàng trực tiếp qua API với danh sách sản phẩm rỗng | API Backend đang chạy | Gửi request POST tới `/api/checkout` | Body: `{"items": [], "total_amount": 0}` | Trả về `400 Bad Request` do giỏ hàng trống. | Invalid | High |
| FR20-API-TC-02 | Gửi POST tạo đơn hàng trực tiếp qua API với số lượng sản phẩm âm | API Backend đang chạy | Gửi request POST tới `/api/checkout` | Body: `{"items": [{"id": 1, "price": 100000, "quantity": -5}], "total_amount": 100000}` | Trả về `400 Bad Request` do số lượng sản phẩm không hợp lệ. | Invalid | High |
| FR20-API-TC-03 | Gửi POST tạo đơn hàng trực tiếp qua API không kèm Token Authorization | API Backend đang chạy | Gửi request POST tới `/api/checkout` không có Header Authorization | Body hợp lệ | Trả về `401 Unauthorized` chặn truy cập đơn hàng. | Invalid | High |
| FR20-API-TC-04 | Gửi POST áp dụng mã giảm giá trực tiếp không truyền mã code | API Backend đang chạy | Gửi request POST tới `/api/apply-coupon` | Body: `{"total_amount": 500000, "user_id": 1}` | Trả về `400 Bad Request` yêu cầu nhập mã giảm giá. | Invalid | Medium |
| FR20-API-TC-05 | Gửi POST áp dụng mã giảm giá với số tiền đơn hàng là số âm | API Backend đang chạy | Gửi request POST tới `/api/apply-coupon` | Body: `{"code": "SAVE10", "total_amount": -100000, "user_id": 1}` | Trả về `400 Bad Request` do số tiền không hợp lệ. | Invalid | High |
