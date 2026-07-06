&lt;!-- File: FR-08_TestReport.md --&gt;

# BÁO CÁO KIỂM THỬ: FR-08 — Thanh Toán & Checkout

**Ngày lập:** 2026-07-06  
**Người lập:** Senior QA Engineer (AI-Assisted)  
**Hệ thống:** EShop Demo — Vietnamese E-Commerce Application  
**Phạm vi:** `POST /api/apply-coupon` · `POST /api/checkout` · `Checkout.jsx`

---

## ⚠️ LỖI BẢO MẬT NGHIÊM TRỌNG — PHÁT HIỆN TRƯỚC KHI PHÂN TÍCH

> **[CRITICAL SECURITY VULNERABILITY]**  
> Trong `Checkout.jsx` (dòng 14, 93–102), biến `editableTotal` được render thành một `<input type="number">` cho phép **người dùng tự sửa tổng tiền** trực tiếp trên giao diện.  
> Backend `POST /api/checkout` (server.js dòng 297–309) và `POST /api/apply-coupon` (dòng 363–441) đều **nhận `total_amount` từ request body mà không hề xác thực lại** so với dữ liệu giỏ hàng thực tế.  
> → Kẻ tấn công có thể thao túng giá trị này để: (1) **thanh toán đơn hàng triệu đồng với giá 1 VND**, (2) **vượt ngưỡng `min_order_amount` của coupon bằng cách tự inflate `total_amount`**.

---

## BƯỚC 1: PHÂN TÍCH MIỀN GIÁ TRỊ (Domain Testing Analysis)

### 1.1. Xác định các biến đầu vào và trạng thái hệ thống

| # | Biến | Nguồn | Kiểu dữ liệu |
|---|------|-------|--------------|
| 1 | `total_amount` | `editableTotal` (Checkout.jsx L.14) — **người dùng tự nhập** | Numeric (Number) |
| 2 | `code` | Input mã coupon (Checkout.jsx L.112) | String |
| 3 | `user_id` | `user?.id` từ AuthContext | Integer \| null |
| 4 | `coupon.min_order_amount` | DB: bảng `coupons` | INTEGER (default 0) |
| 5 | `coupon.max_uses_per_user` | DB: bảng `coupons` | INTEGER (default 1) |
| 6 | `coupon.expired_at` | DB: bảng `coupons` | DATETIME |
| 7 | `coupon.is_active` | DB: bảng `coupons` | INTEGER (0 \| 1) |

### 1.2. Phân tích Miền của `total_amount`

Logic kiểm tra duy nhất ở backend (`server.js` dòng 379):
```javascript
if (total_amount > coupon.min_order_amount) { ... }
```

**Điểm nguy hiểm:** Backend KHÔNG tính lại `total_amount` từ giỏ hàng. Giá trị này hoàn toàn do client gửi lên.

#### Miền hợp lệ (Valid Equivalence Classes — VEC)

| Ký hiệu | Mô tả | Điều kiện |
|---------|-------|-----------|
| **VEC-TA-1** | Tổng tiền hợp lệ bình thường (theo UI) | `total_amount > min_order_amount` |
| **VEC-TA-2** | Tổng tiền bị **giả mạo tăng cao** (attacker inflate) | Giá trị cao hơn tổng thực tế của giỏ, nhưng `> min_order_amount` → backend vẫn chấp nhận |
| **VEC-TA-3** | Tổng tiền bị **giả mạo giảm xuống** để qua checkout | Giá trị cực nhỏ (1, 0, -1) → bypass giá trị thực |

#### Miền không hợp lệ (Invalid Equivalence Classes — IEC)

| Ký hiệu | Mô tả | Điều kiện |
|---------|-------|-----------|
| **IEC-TA-1** | `total_amount ≤ min_order_amount` | Backend từ chối áp dụng coupon |
| **IEC-TA-2** | `total_amount` âm | Giá trị không hợp lý mặt nghiệp vụ |
| **IEC-TA-3** | `total_amount = 0` | Đơn hàng rỗng |
| **IEC-TA-4** | `total_amount` là string/null/NaN | Lỗi kiểu dữ liệu |

### 1.3. Coupon Seeded trong Database (dữ liệu thực tế)

| Mã | Loại | Giảm | `min_order_amount` | `max_uses_per_user` | Hết hạn |
|----|------|------|-------------------|---------------------|---------|
| SAVE10 | percent | 10% | **300.000 ₫** | 1 | 2099-12-31 (còn hạn) |
| BIGBUY | fixed | 50.000 ₫ | **500.000 ₫** | 1 | 2099-12-31 (còn hạn) |
| VIP100 | fixed | 100.000 ₫ | **300.000 ₫** | **2** | 2099-12-31 (còn hạn) |
| EXPIRED | percent | 20% | 100.000 ₫ | 1 | 2020-01-01 **(đã hết hạn)** |

### 1.4. Phân tích Miền của `code`

| Miền | Điều kiện | Phân loại |
|------|-----------|-----------|
| Mã tồn tại và `is_active = 1` | Coupon hợp lệ | VEC |
| Mã tồn tại nhưng `is_active = 0` | Coupon bị vô hiệu hoá | IEC |
| Mã không tồn tại trong DB | Trả về 404 | IEC |
| Chuỗi rỗng `""` | Frontend chặn nếu trim = empty | IEC |
| Null / không truyền | Backend trả 400 (`!code`) | IEC |

---

## BƯỚC 2: PHÂN TÍCH GIÁ TRỊ BIÊN (Boundary Value Analysis)

### 2.1. Biên của `total_amount` so với `min_order_amount`

Lấy coupon **SAVE10** làm mốc: `min_order_amount = 300.000`  
Logic backend: **STRICTLY GREATER THAN** (`total_amount > 300000`)

| Vị trí biên | Giá trị `total_amount` | Kết quả mong đợi |
|-------------|----------------------|-----------------|
| **Just below** (ngay dưới) | `299.999` | ❌ Từ chối — "chưa đủ giá trị tối thiểu" |
| **On boundary** (đúng biên) | `300.000` | ❌ Từ chối — điều kiện là `>`, không phải `>=` |
| **Just above** (ngay trên) | `300.001` | ✅ Chấp nhận — áp dụng coupon thành công |

#### Biên đặc biệt cho lỗi `editableTotal`:

| Vị trí | Giá trị đầu vào (`editableTotal`) | Hành vi thực tế (BUG) |
|--------|-----------------------------------|----------------------|
| Cực tiểu dương | `1` | Checkout với 1 VND → Đơn hàng triệu đồng lưu vào DB với `total_amount = 1` |
| Zero | `0` | `0 > 300000` = false → coupon bị từ chối; nhưng checkout vẫn thành công với 0 ₫ |
| Âm | `-1` | `-1 > 300000` = false → coupon từ chối; checkout với `-1` ₫ được lưu vào DB |
| Inflate (attacker) | `999999999` | `999999999 > 300000` = true → coupon áp dụng, nhưng `final_amount` được tính trên số giả |

### 2.2. Biên của `max_uses_per_user`

Lấy coupon **VIP100**: `max_uses_per_user = 2`  
Logic backend (`server.js` L.391): `result.usage_count >= coupon.max_uses_per_user`

| Vị trí biên | Số lần đã dùng | Kết quả |
|-------------|---------------|---------|
| **Just below** | `usage_count = 1` | ✅ Được phép áp dụng (1 < 2) |
| **On boundary** | `usage_count = 2` | ❌ Từ chối — "đã đạt giới hạn" |
| **Just above** | `usage_count = 3` | ❌ Từ chối (>= 2) |

### 2.3. Biên của `expired_at`

| Loại | Giá trị | Kết quả |
|------|---------|---------|
| Coupon còn hạn | `2099-12-31` | ✅ Hợp lệ |
| Coupon hết hạn đúng hôm nay | `2026-07-06T23:59:59` | ❌ Expired (nếu `now > expiry`) |
| Coupon đã hết hạn | `2020-01-01` (EXPIRED) | ❌ "Mã giảm giá đã hết hạn" |

---

## BƯỚC 3: BẢNG TEST CASE TỔNG HỢP

### 3.1. Nhóm A — Kiểm thử `total_amount` (Domain Testing + BVA) — Lỗi `editableTotal`

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Loại |
|--------------|-------|----------------|-----------------|----------------|------|
| **TC-FR08-001** | Tổng tiền bị giả mạo xuống 1 VND — bypass checkout | `POST /api/checkout` với `total_amount: 1`, `shipping_address: "123 Test"` | ❌ Hệ thống phải từ chối — total không khớp giỏ hàng | ✅ Thành công (BUG: đơn lưu `total_amount = 1`) | **Invalid** |
| **TC-FR08-002** | Tổng tiền = 0 — đơn hàng rỗng | `POST /api/checkout` với `total_amount: 0` | ❌ Từ chối — tổng tiền không thể = 0 | ✅ Thành công (BUG: đơn lưu `total_amount = 0`) | **Invalid** |
| **TC-FR08-003** | Tổng tiền âm | `POST /api/checkout` với `total_amount: -1` | ❌ Từ chối — giá trị âm không hợp lệ | ✅ Thành công (BUG: đơn lưu `-1`) | **Invalid** |
| **TC-FR08-004** | Tổng tiền âm cực lớn | `POST /api/checkout` với `total_amount: -99999999` | ❌ Từ chối | ✅ Thành công (BUG) | **Invalid** |
| **TC-FR08-005** | Tổng tiền hợp lệ bình thường | `POST /api/checkout` với `total_amount: 1500000` (khớp giỏ hàng thực) | ✅ Checkout thành công, đơn được tạo | ✅ Thành công | **Valid** |
| **TC-FR08-006** | Tổng tiền inflate — giả mạo số lớn | `POST /api/checkout` với `total_amount: 999999999` (giỏ thực chỉ 150k) | ❌ Từ chối — không khớp giỏ hàng | ✅ Thành công (BUG: đơn lưu 999 triệu) | **Invalid** |
| **TC-FR08-007** | `total_amount` là null | `POST /api/checkout` với `total_amount: null` | ❌ Từ chối — thiếu dữ liệu bắt buộc | ✅ Thành công (BUG: lưu null vào DB) | **Invalid** |
| **TC-FR08-008** | `total_amount` là string | `POST /api/checkout` với `total_amount: "abc"` | ❌ Từ chối — sai kiểu dữ liệu | ✅ Thành công (BUG: lưu "abc" vào DB) | **Invalid** |

---

### 3.2. Nhóm B — Kiểm thử Coupon `total_amount` vs `min_order_amount` (BVA — SAVE10, min=300.000)

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|--------------|-------|----------------|-----------------|------|
| **TC-FR08-010** | Just below — tổng < tối thiểu | `code: "SAVE10"`, `total_amount: 299999` | ❌ "Đơn hàng chưa đủ giá trị tối thiểu 300.000 ₫" | **Invalid** |
| **TC-FR08-011** | On boundary — tổng = tối thiểu chính xác | `code: "SAVE10"`, `total_amount: 300000` | ❌ Từ chối (điều kiện `>` không phải `>=`) | **Invalid** |
| **TC-FR08-012** | Just above — tổng ngay trên tối thiểu | `code: "SAVE10"`, `total_amount: 300001` | ✅ Áp dụng coupon thành công | **Valid** |
| **TC-FR08-013** | Tổng hợp lệ điển hình | `code: "SAVE10"`, `total_amount: 500000` | ✅ Giảm 10% → `final_amount = 450000` | **Valid** |
| **TC-FR08-014** | **[Exploit]** Inflate `total_amount` vượt min_order | `code: "SAVE10"`, `total_amount: 999999` (giỏ thực chỉ 150k) | ❌ Backend phải xác thực lại; thực tế: ✅ coupon áp dụng (BUG) | **Invalid** |
| **TC-FR08-015** | **[Exploit]** Dùng `editableTotal = 300001` để bypass min_order của BIGBUY (min=500k) | `code: "SAVE10"`, `editableTotal` tự sửa = `300001` | ❌ Phải từ chối vì total thực < 300k; thực tế: ✅ được áp dụng (BUG) | **Invalid** |

---

### 3.3. Nhóm C — Kiểm thử Coupon `total_amount` vs `min_order_amount` (BVA — BIGBUY, min=500.000)

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|--------------|-------|----------------|-----------------|------|
| **TC-FR08-020** | Just below | `code: "BIGBUY"`, `total_amount: 499999` | ❌ Từ chối | **Invalid** |
| **TC-FR08-021** | On boundary | `code: "BIGBUY"`, `total_amount: 500000` | ❌ Từ chối (`>` không phải `>=`) | **Invalid** |
| **TC-FR08-022** | Just above | `code: "BIGBUY"`, `total_amount: 500001` | ✅ Áp dụng: giảm 50.000 ₫, `final_amount = 450001` | **Valid** |
| **TC-FR08-023** | **[Exploit]** Inflate vượt min BIGBUY | `code: "BIGBUY"`, `total_amount: 500001` nhưng giỏ thực chỉ 28k | ❌ Phải từ chối (BUG: Chấp nhận) | **Invalid** |

---

### 3.4. Nhóm D — Kiểm thử `max_uses_per_user` (BVA — VIP100, max=2)

| Test Case ID | Mô tả | Điều kiện tiền đề | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|--------------|-------|-------------------|----------------|-----------------|------|
| **TC-FR08-030** | Usage = 0 (chưa dùng lần nào) | `usage_count = 0` | `code: "VIP100"`, `total_amount: 400000`, `user_id: 2` | ✅ Áp dụng thành công | **Valid** |
| **TC-FR08-031** | Just below max — usage = 1 | `usage_count = 1` | `code: "VIP100"`, `total_amount: 400000`, `user_id: 2` | ✅ Áp dụng thành công (1 < 2) | **Valid** |
| **TC-FR08-032** | On boundary — usage = 2 | `usage_count = 2` | `code: "VIP100"`, `total_amount: 400000`, `user_id: 2` | ❌ "Đã đạt giới hạn" (2 >= 2) | **Invalid** |
| **TC-FR08-033** | Above max — usage = 3 | `usage_count = 3` | `code: "VIP100"`, `total_amount: 400000`, `user_id: 2` | ❌ Từ chối | **Invalid** |
| **TC-FR08-034** | `user_id = null` — guest checkout | N/A | `code: "VIP100"`, `total_amount: 400000`, `user_id: null` | ✅ Áp dụng (bỏ qua nhánh usage check — BUG tiềm ẩn: guest lạm dụng không giới hạn) | **Valid** |

---

### 3.5. Nhóm E — Kiểm thử `code` (Domain Testing)

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|--------------|-------|----------------|-----------------|------|
| **TC-FR08-040** | Mã coupon hợp lệ, còn hạn | `code: "SAVE10"`, `total_amount: 500000` | ✅ Thành công | **Valid** |
| **TC-FR08-041** | Mã coupon hết hạn | `code: "EXPIRED"`, `total_amount: 500000` | ❌ "Mã giảm giá đã hết hạn" | **Invalid** |
| **TC-FR08-042** | Mã không tồn tại | `code: "NONEXIST"`, `total_amount: 500000` | ❌ 404 "Mã không tồn tại" | **Invalid** |
| **TC-FR08-043** | Mã để trống | `code: ""`, `total_amount: 500000` | ❌ 400 "Vui lòng nhập mã giảm giá" | **Invalid** |
| **TC-FR08-044** | Mã chữ thường (lowercase) | `code: "save10"`, `total_amount: 500000` | ✅ Thành công (frontend auto uppercase; nếu gọi API trực tiếp: phụ thuộc SQLite case-sensitivity) | **Valid** |
| **TC-FR08-045** | Mã chứa ký tự đặc biệt (SQL Injection) | `code: "' OR '1'='1"`, `total_amount: 500000` | ❌ Từ chối — DB query dùng parameterized (`?`) nên an toàn | **Invalid** |
| **TC-FR08-046** | Bypass API trực tiếp — bỏ qua frontend uppercase | `POST /api/apply-coupon` với `code: "save10"` (lowercase, bypass UI) | Phụ thuộc SQLite collation — Cần kiểm tra thực tế | **Invalid** |

---

### 3.6. Nhóm F — API Bypass (Kiểm thử trực tiếp qua curl/Postman)

| Test Case ID | Mô tả | Phương thức | Request Body | Kết quả mong đợi | Loại |
|--------------|-------|-------------|--------------|-----------------|------|
| **TC-FR08-050** | Checkout với `total_amount = 1` qua API trực tiếp | `POST /api/checkout` | `{"total_amount": 1, "shipping_address": "Test"}` | ❌ Phải từ chối (BUG: 200 OK) | **Invalid** |
| **TC-FR08-051** | Apply coupon SAVE10 với total thực tế dưới ngưỡng nhưng gửi giá trị inflate | `POST /api/apply-coupon` | `{"code":"SAVE10","total_amount":999999,"user_id":2}` | ❌ Phải xác thực lại (BUG: Coupon áp dụng thành công) | **Invalid** |
| **TC-FR08-052** | Checkout không có Authorization header | `POST /api/checkout` (no token) | `{"total_amount": 100000}` | ❌ 401 Unauthorized | **Invalid** |
| **TC-FR08-053** | Apply coupon không có `user_id` — test guest exploitation | `POST /api/apply-coupon` | `{"code":"VIP100","total_amount":400000}` (không có `user_id`) | ✅ Thành công (BUG: guest không bị giới hạn số lần dùng) | **Invalid** |

---

## BẢNG TÓM TẮT LỖI PHÁT HIỆN

| # | Lỗi | Mức độ | File | Dòng |
|---|-----|--------|------|------|
| 🔴 BUG-01 | `editableTotal` cho phép người dùng tự sửa `total_amount` trên UI | **CRITICAL** | Checkout.jsx | L.14, L.93–102 |
| 🔴 BUG-02 | Backend `POST /api/checkout` không xác thực `total_amount` vs giỏ hàng thực | **CRITICAL** | server.js | L.297–309 |
| 🔴 BUG-03 | Backend `POST /api/apply-coupon` nhận `total_amount` từ client, không tính lại server-side | **CRITICAL** | server.js | L.363–441 |
| 🟠 BUG-04 | Guest user (`user_id = null`) không bị kiểm tra `max_uses_per_user` | **HIGH** | server.js | L.386 |
| 🟡 BUG-05 | Boundary condition: điều kiện `>` thay vì `>=` có thể gây nhầm lẫn nghiệp vụ | **MEDIUM** | server.js | L.379 |
| 🟡 BUG-06 | `total_amount` âm hoặc bằng 0 được lưu vào DB `orders` không có validation | **HIGH** | server.js | L.302–303 |

---
