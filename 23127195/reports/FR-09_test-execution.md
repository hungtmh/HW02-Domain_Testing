# Test Execution — FR-09: Mã Giảm Giá (Discount Coupons)

**MSSV:** 23127195  
**Ngày thực thi:** 2026-06-09  
**Môi trường thử nghiệm:** Windows 10, Node.js v18+, SQLite, Chrome / React Web (:5173)  
**Người thực hiện:** 23127195  

---

## 1. Kết quả tổng hợp (Test Summary)

| Chỉ số (Metric) | Số lượng (Count) |
|-----------------|------------------|
| Tổng số kịch bản thiết kế | 13 |
| Đã thực thi (Executed) | 12 |
| **ĐẠT (Pass)** | 5 |
| **KHÔNG ĐẠT (Fail)** | 7 |
| Chưa chạy (Not run) | 1 |

---

## 2. Nhật ký thực thi API Layer (`POST /api/apply-coupon`)

Thực hiện kiểm thử API trực tiếp bằng PowerShell `Invoke-RestMethod` (chạy trên cổng `3000` của local backend):

| TC-ID | Dữ liệu đầu vào (Request Body) | HTTP Code | Kết quả thực tế (Actual Result) | Kết quả mong đợi (Expected) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-----------------------------|-----------|---------------------------------|----------------------------|---------------------|-----------------|
| **DT-01** | code=`"SAVE10"`, total=`350000`, user_id=`2` | 200 OK | `discount_amount: -3150000`, `final_amount: 3500000` | Áp dụng thành công, giảm 10% (tiết kiệm 35k, thành tiền 315k) | **FAIL** | [BUG-002](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_bug-report.md#BUG-002) |
| **DT-02** | code=`"BIGBUY"`, total=`550000`, user_id=`2` | 200 OK | `discount_amount: 50000`, `final_amount: 500000` | Áp dụng thành công, giảm 50k, thành tiền 500k | **PASS** | — |
| **DT-03** | code=`"NOSUCH"`, total=`350000` | 404 Not Found | `{"error":"Mã giảm giá không tồn tại..."}` | Từ chối, báo mã không tồn tại | **PASS** | — |
| **DT-04** | code=`""` | 400 Bad Request | `{"error":"Vui lòng nhập mã giảm giá"}` | Từ chối, báo rỗng | **PASS** | — |
| **DT-05** | code=`"EXPIRED"`, total=`150000`, user_id=`2` | 400 Bad Request | `{"error":"Mã giảm giá đã hết hạn"}` | Từ chối, báo hết hạn | **PASS** | — |
| **DT-06** | code=`"SAVE10"`, total=`250000`, user_id=`2` | 400 Bad Request | `{"error":"Đơn hàng chưa đủ giá trị..."}` | Từ chối, báo chưa đủ ngưỡng | **PASS** | — |
| **DT-07** | code=`"SAVE10"`, total=`350000`, user_id=`null` (Không gửi token) | 200 OK | Áp dụng thành công | Từ chối, yêu cầu đăng nhập theo C4 | **FAIL** | [BUG-003](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_bug-report.md#BUG-003) |
| **DT-08** | code=`"SAVE10"`, total=`350000`, user_id=`2` (đã lưu 1 lần dùng trước đó) | 400 Bad Request | `{"error":"Bạn đã sử dụng mã này 1 lần..."}` | Từ chối vì đạt giới hạn lượt sử dụng | **PASS** | — |
| **DT-09** | code=`"DISABLED"`, total=`350000` | 404 | Báo lỗi không tồn tại | Từ chối | **PASS** | — |
| **DT-10** | code=`"SAVE10"`, total=`350000`, user_id=`999` (ID giả mạo, token user 2) | 200 OK | Áp dụng thành công | Từ chối/Kiểm tra chéo JWT token bảo mật | **FAIL** | [BUG-004](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_bug-report.md#BUG-004) |
| **BV-02** | code=`"SAVE10"`, total=`300000`, user_id=`2` | 400 Bad Request | `{"error":"Đơn hàng chưa đủ giá trị..."}` | Chấp nhận vì đơn hàng bằng đúng ngưỡng 300,000 | **FAIL** | [BUG-001](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_bug-report.md#BUG-001) |
| **BV-03** | code=`"SAVE10"`, total=`300001`, user_id=`2` | 200 OK | Áp dụng thành công | Chấp nhận | **PASS** | — |

---

## 3. Nhật ký thực thi UI / Code Review (Frontend Web)

| TC-ID | Nội dung kiểm thử | Kết quả thực tế (Code & UI) | Kết quả mong đợi (SRS) | Trạng thái (Result) | Mã lỗi (Bug ID) |
|-------|-------------------|-----------------------------|------------------------|---------------------|-----------------|
| **DT-11** | Hiển thị thông báo sau khi áp dụng coupon | Render thông báo màu xanh/đỏ dưới input | Hiển thị thông báo trực quan | **PASS** | — |
| **FR-08** | Cho phép sửa đổi tổng thanh toán trên UI | Ô nhập "Tổng tiền thanh toán" cho phép người dùng nhập tự do | Không cho phép người dùng chỉnh sửa trực tiếp | **FAIL** | [BUG-005](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_bug-report.md#BUG-005) |
