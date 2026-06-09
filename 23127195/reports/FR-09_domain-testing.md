# Domain Testing — FR-09: Mã Giảm Giá (Discount Coupons)

**MSSV:** 23127195  
**Ngày:** 2026-06-09  
**SUT:** Backend API `POST /api/apply-coupon` + Giao diện Checkout (`http://localhost:5173/checkout`)

---

## Bước 1 — Phạm vi và SUT

### Tài liệu Đặc tả (SRS FR-09)
Hệ thống áp dụng giảm giá khi người dùng nhập mã giảm giá tại bước Checkout. Có **5 điều kiện** bắt buộc phải thỏa mãn:
1. **C1 (Mã tồn tại & hoạt động):** Mã phải tồn tại trong cơ sở dữ liệu và đang hoạt động (`is_active = 1`).
2. **C2 (Còn hạn sử dụng):** Ngày hiện tại phải trước ngày hết hạn (`expired_at`).
3. **C3 (Đủ ngưỡng đơn hàng):** Tổng đơn hàng phải lớn hơn hoặc bằng (`>=`) giá trị `min_order_amount`.
4. **C4 (Đã đăng nhập):** Người dùng phải có Token JWT hợp lệ gửi kèm.
5. **C5 (Chưa dùng hết lượt):** Số lần người dùng đã sử dụng mã này phải nhỏ hơn (`<`) giới hạn `max_uses_per_user`.

**Công thức tính toán giảm giá:**
- Loại `percent`: `discount_amount = total × discount_value / 100`
- Loại `fixed`: `discount_amount = discount_value`
- `final_amount = total - discount_amount`

### Các file mã nguồn liên quan
- **Frontend Web:** [Checkout.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Checkout.jsx) (dòng 22-38, 105-134)
- **Backend API:** [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js) (dòng 363–441)
- **Database:** [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js) (dòng 29-38 bảng `coupons`, dòng 41-46 bảng `coupon_usage`, dòng 106-111 seed dữ liệu coupons)

---

## Bước 2 — Input Variables (Biến đầu vào)

| ID | Biến | Kiểu dữ liệu | Nguồn | Ràng buộc từ SRS |
|----|------|--------------|-------|------------------|
| V1 | `code` | String | Form UI / API Body | Mã phải tồn tại và có `is_active = 1` |
| V2 | `total_amount` | Integer | Giỏ hàng / API Body | Phải lớn hơn hoặc bằng `min_order_amount` |
| V3 | `token` | String (JWT) | Headers | Token phải hợp lệ (người dùng đã đăng nhập) |
| V4 | `user_id` | Integer | Token / API Body | Cần thiết để đếm số lần sử dụng mã của user |
| V5 | `current_time` | Datetime | System | Phải trước ngày hết hạn `expired_at` của mã |

**Bộ giá trị hợp lệ mặc định (để kiểm thử đơn lỗi):**
- `code`: `"SAVE10"` (loại percent, giảm 10%, ngưỡng tối thiểu 300,000 ₫)
- `total_amount`: `350000` (thỏa mãn ngưỡng tối thiểu 300,000 ₫)
- `token`: *[Token hợp lệ của tài khoản user test]*
- `user_id`: `2` (user test)
- `current_time`: *[Ngày hiện tại của hệ thống]*

---

## Bước 3 — Domains (Miền giá trị)

| Biến | Miền hợp lệ (Valid Domain) | Miền không hợp lệ (Invalid Domain) | Giá trị đặc biệt (Special/Edge Values) |
|------|----------------------------|-----------------------------------|---------------------------------------|
| **code** | Mã có trong DB và `is_active = 1` (`SAVE10`, `BIGBUY`, `VIP100`) | Mã không tồn tại, mã có `is_active = 0` | Để trống `""`, mã chứa ký tự đặc biệt, SQL Injection |
| **total_amount** | Giá trị `>= min_order_amount` | Giá trị `< min_order_amount` | Bằng 0, số âm, giá trị cực lớn (overflow) |
| **token** | Token JWT hợp lệ và chưa hết hạn | Không gửi kèm token, token sai chữ ký, token hết hạn | Token rỗng |
| **user_id** | ID của user đã đăng nhập khớp token | ID của user khác (giả mạo), ID không tồn tại | `NULL`, rỗng |

---

## Bước 4 — Equivalence Partitions (Phân vùng tương đương)

| EP-ID | Loại vùng | Biến tác động | Mô tả phân vùng tương đương | Giá trị đại diện |
|-------|-----------|---------------|-----------------------------|------------------|
| **EP-CP01** | Hợp lệ | code | Mã tồn tại, đang hoạt động | `"SAVE10"`, `"BIGBUY"` |
| **EP-CP02** | Không hợp lệ | code | Mã không tồn tại | `"INVALID_CODE"` |
| **EP-CP03** | Không hợp lệ | code | Mã tồn tại nhưng đã bị vô hiệu hóa | `"DISABLED_CODE"` |
| **EP-CP04** | Không hợp lệ | code | Mã giảm giá bị bỏ trống | `""` |
| **EP-EXP1** | Hợp lệ | current_time | Còn hạn sử dụng (ngày hiện tại < expired_at) | `"SAVE10"` (hạn 2099) |
| **EP-EXP2** | Không hợp lệ | current_time | Đã hết hạn sử dụng (ngày hiện tại >= expired_at) | `"EXPIRED"` (hạn 2020) |
| **EP-AMT1** | Hợp lệ | total_amount | Tổng đơn hàng `>= min_order_amount` | `total_amount = 350000` (mã `SAVE10`) |
| **EP-AMT2** | Không hợp lệ | total_amount | Tổng đơn hàng `< min_order_amount` | `total_amount = 250000` (mã `SAVE10`) |
| **EP-AUTH1**| Hợp lệ | token | Đã đăng nhập, token hợp lệ | `Bearer <valid_token>` |
| **EP-AUTH2**| Không hợp lệ | token | Chưa đăng nhập (không gửi token) | *Không gửi Header Authorization* |
| **EP-USG1** | Hợp lệ | user_id | Số lần đã sử dụng mã < max_uses_per_user | Sử dụng 0 lần (mã `SAVE10` limit 1) |
| **EP-USG2** | Không hợp lệ | user_id | Số lần đã sử dụng mã >= max_uses_per_user | Sử dụng 1 lần (mã `SAVE10` limit 1) |
| **EP-TYP1** | Hợp lệ | coupon type | Loại mã giảm giá theo phần trăm (`percent`) | `"SAVE10"` (giảm 10%) |
| **EP-TYP2** | Hợp lệ | coupon type | Loại mã giảm giá cố định (`fixed`) | `"BIGBUY"` (giảm 50,000 ₫) |

---

## Bước 5 — Constraints (Các ràng buộc nghiệp vụ)

| C-ID | Ràng buộc chéo / Nghiệp vụ | Loại ràng buộc | Kết quả kỳ vọng |
|------|---------------------------|----------------|-----------------|
| **C-01** | Tất cả điều kiện đồng thời | Ràng buộc chéo | Chỉ áp dụng giảm giá khi cả 5 điều kiện (C1, C2, C3, C4, C5) đều thỏa mãn. |
| **C-02** | Loại mã `percent` | Tính toán | Tiết kiệm `discount_amount = total * discount_value / 100`. |
| **C-03** | Loại mã `fixed` | Tính toán | Tiết kiệm `discount_amount = discount_value`. |
| **C-04** | Kiểm tra chéo user_id | Ràng buộc bảo mật | Không cho phép gửi kèm `user_id` giả mạo trong body nếu không có token JWT khớp tương ứng. |

---

## Bước 6 — Test Cases thiết kế từ Domain Testing

*Mặc định các trường còn lại sẽ giữ giá trị hợp lệ để thực hiện kỹ thuật Single-Fault.*

| TC-ID | Mô tả kịch bản kiểm thử | Input thực tế đầu vào | Kết quả mong đợi theo SRS | Phân vùng EP / Ràng buộc |
|-------|-------------------------|-----------------------|---------------------------|-------------------------|
| **DT-01** | Áp dụng thành công mã `SAVE10` (loại percent) | code=`"SAVE10"`, total=`350000`, user_id=`2` (đã đăng nhập) | Áp dụng thành công, giảm `35,000 ₫`, thành tiền `315,000 ₫` | EP-CP01, EP-TYP1, C-02 |
| **DT-02** | Áp dụng thành công mã `BIGBUY` (loại fixed) | code=`"BIGBUY"`, total=`550000`, user_id=`2` (đã đăng nhập) | Áp dụng thành công, giảm `50,000 ₫`, thành tiền `500,000 ₫` | EP-CP01, EP-TYP2, C-03 |
| **DT-03** | Áp dụng mã không tồn tại | code=`"NOSUCH"`, total=`350000` | Báo lỗi: "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa" | EP-CP02 |
| **DT-04** | Áp dụng mã giảm giá bị rỗng | code=`""`, total=`350000` | Báo lỗi yêu cầu nhập mã giảm giá | EP-CP04 |
| **DT-05** | Áp dụng mã giảm giá đã hết hạn | code=`"EXPIRED"`, total=`150000`, user_id=`2` (đã đăng nhập) | Báo lỗi: "Mã giảm giá đã hết hạn" | EP-EXP2 |
| **DT-06** | Áp dụng mã khi tổng tiền chưa đạt ngưỡng tối thiểu | code=`"SAVE10"`, total=`250000`, user_id=`2` (đã đăng nhập) | Báo lỗi đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ | EP-AMT2 |
| **DT-07** | Áp dụng mã khi chưa đăng nhập (Guest) | code=`"SAVE10"`, total=`350000` (Không gửi kèm token) | Từ chối áp dụng mã, báo lỗi yêu cầu đăng nhập | EP-AUTH2 |
| **DT-08** | Áp dụng mã vượt quá giới hạn sử dụng của user | code=`"SAVE10"`, total=`350000`, user_id=`2` (đã sử dụng mã này 1 lần trước đó) | Báo lỗi người dùng đã sử dụng mã này đạt giới hạn | EP-USG2 |
| **DT-09** | Áp dụng mã bị vô hiệu hóa (`is_active = 0`) | code=`"DISABLED"`, total=`350000` | Báo lỗi mã giảm giá không tồn tại hoặc bị vô hiệu hóa | EP-CP03 |
| **DT-10** | Giả mạo `user_id` trong request body để bypass lượt dùng | code=`"SAVE10"`, total=`350000`, body chứa `user_id=3` nhưng token JWT là của `user_id=2` | Từ chối hoặc tự động đếm lượt dùng dựa trên JWT, không tin tưởng `user_id` từ request body | C-04, C-01 |

---

## Tóm tắt Coverage

- **Tổng số phân vùng EP:** 14 phân vùng.
- **Tổng số Test Cases thiết kế:** 10 test cases.
- **Mục tiêu phủ:** Toàn bộ 5 điều kiện nghiệp vụ và các loại hình giảm giá trong hệ thống.
