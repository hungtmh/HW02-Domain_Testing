# Boundary Value Analysis — FR-09: Mã Giảm Giá (Discount Coupons)

**MSSV:** 23127195  
**Ngày:** 2026-06-09  
**SUT:** Backend API `POST /api/apply-coupon` + Giao diện Checkout

---

## Bước 1 — Xác định các biên (Boundaries) từ đặc tả SRS

Dựa vào SRS FR-09, ta xác định các biên sau:

| B-ID | Biến | Ràng buộc SRS | Điểm biên dưới (Min) | Điểm biên trên (Max) | Kiểu biên |
|------|------|---------------|----------------------|----------------------|-----------|
| **B-MIN-AMT** | `total_amount` | Phải `>= min_order_amount` | `min_order_amount` | Không giới hạn | Ngưỡng giá trị số |
| **B-EXP-DATE**| `current_time` | Phải `< expired_at` | Không có | `expired_at` | Ngày giờ |
| **B-USG-LIMIT**| `usage_count` | Phải `< max_uses_per_user` | Không có | `max_uses_per_user` | Số lần (count) |

---

## Bước 2 — Xác định các điểm kiểm thử biên (BVA Points)

### 1. Phân tích biên cho ngưỡng đơn hàng tối thiểu (B-MIN-AMT)
*Sử dụng mã `SAVE10` (`min_order_amount = 300000 ₫`). Giữ các điều kiện khác hợp lệ.*
- **Sát dưới biên (Min - 1):** `total_amount = 299999` -> Kỳ vọng: **Từ chối (Reject)**
- **Tại biên (Min):** `total_amount = 300000` -> Kỳ vọng: **Chấp nhận (Accept)**
- **Sát trên biên (Min + 1):** `total_amount = 300001` -> Kỳ vọng: **Chấp nhận (Accept)**

### 2. Phân tích biên do lỗi cài đặt thực tế (Implementation-specific boundary)
Do Backend kiểm tra điều kiện `total_amount > coupon.min_order_amount` (lớn hơn hẳn) thay vì `>=` (lớn hơn hoặc bằng):
- **Tại biên `total_amount = 300000`:** SRS kỳ vọng **Chấp nhận** | Backend thực tế: **Từ chối** (Báo đơn hàng chưa đủ giá trị tối thiểu).

### 3. Phân tích biên cho giới hạn lượt sử dụng của người dùng (B-USG-LIMIT)
*Sử dụng mã `SAVE10` (`max_uses_per_user = 1`). Giữ các điều kiện khác hợp lệ.*
- **Dưới giới hạn (Limit - 1):** Đã dùng `0` lần -> Kỳ vọng: **Chấp nhận**
- **Tại giới hạn (Limit):** Đã dùng `1` lần -> Kỳ vọng: **Từ chối**
- **Vượt giới hạn (Limit + 1):** Đã dùng `2` lần -> Kỳ vọng: **Từ chối**

### 4. Phân tích biên cho thời hạn của mã giảm giá (B-EXP-DATE)
- **Trước ngày hết hạn 1 ngày:** (Hợp lệ) -> Kỳ vọng: **Chấp nhận**
- **Đúng ngày hết hạn:** (Hết hạn) -> Kỳ vọng: **Từ chối**

---

## Bước 3 — Danh sách Test Cases thiết kế từ BVA

*Mặc định: `code="SAVE10"`, `user_id=2` (đã đăng nhập), `current_time` hợp lệ.*

| TC-ID | Input (`total_amount`) | Vùng biên kiểm tra | Expected (SRS) | Expected (Backend thực tế) | Kết quả kỳ vọng |
|-------|------------------------|-------------------|----------------|----------------------------|-----------------|
| **BV-01** | `299999` | Đơn hàng Min - 1 | Từ chối | Từ chối | Từ chối |
| **BV-02** | `300000` | Đơn hàng Min | Chấp nhận | Từ chối (do lỗi `>`) | **FAIL** (Sai logic biên) |
| **BV-03** | `300001` | Đơn hàng Min + 1 | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-04** | `total_amount = 550000`, coupon=`"BIGBUY"` (ngưỡng 500k) | Đơn hàng Min + 50k | Chấp nhận | Chấp nhận | Chấp nhận |
| **BV-05** | `total_amount = 500000`, coupon=`"BIGBUY"` | Đơn hàng Min | Chấp nhận | Từ chối (do lỗi `>`) | **FAIL** (Sai logic biên) |
| **BV-06** | `total_amount = 499999`, coupon=`"BIGBUY"` | Đơn hàng Min - 1 | Từ chối | Từ chối | Từ chối |
| **BV-07** | `total_amount = 300000`, coupon=`"VIP100"` (lượt dùng = 2) | Lượt dùng 1/2 (Limit - 1) | Chấp nhận | Chấp nhận (nếu chưa dùng lần nào) | Chấp nhận |
| **BV-08** | `total_amount = 300000`, coupon=`"VIP100"` (lượt dùng = 2) | Lượt dùng 2/2 (Limit) | Từ chối | Từ chối | Từ chối |

---

## Bước 4 — Kịch bản biên Robustness / Edge cases bổ sung

| TC-ID | Đầu vào kiểm thử | Mục đích kiểm tra | Kết quả mong đợi |
|-------|------------------|-------------------|------------------|
| **BV-R01** | `total_amount = 0` | Giá trị tối thiểu âm/bằng không | Từ chối |
| **BV-R02** | `total_amount = -100` | Giá trị âm | Từ chối |
| **BV-R03** | code = `null` | Giá trị null | Từ chối, báo lỗi |
