# Main Testing Report - EShop Domain Testing

**Họ và tên:** Nguyễn Tấn Thắng  
**Nhóm:** Nhóm 08  
**MSSV:** 23127259  
**Ngày chạy test/evidence:** 2026-07-05 20:13 ICT  
**Ngày đồng bộ báo cáo:** 2026-07-06  
**SUT:** `/Users/thangnhi/Downloads/eshop-sut`  
**Backend:** `http://localhost:3000/api`

---

## 1. Test Run Evidence

Backend đã chạy sẵn trên port `3000`, sau đó em chạy API test bằng Node `fetch` và kiểm tra SQLite trực tiếp để xác nhận state sau request. Các test có dữ liệu ghi DB dùng prefix `live_hw02_1783257224503`; sau test đã cleanup và kiểm tra lại không còn user/product test.

| Check | Result |
|-------|--------|
| Admin login `admin@eshop.com / Admin123!` | PASS - HTTP 200, có JWT |
| Normal user test login | PASS - HTTP 200, có JWT |
| Cleanup product/user test | PASS - DB không còn record `live_hw02_%` |
| `frontend-web npm run lint` | FAIL - 23 errors, 1 warning có sẵn trong source |
| `frontend-admin npm run lint` | FAIL - 4 errors có sẵn trong source |

Ảnh/video evidence được lưu trong các thư mục `reports/*_bugs/` và là minh chứng từ quá trình thao tác UI/API trực tiếp trên EShop SUT. Riêng FR-07 BUG-003 dùng video `.mov` để thể hiện thao tác bấm `Xóa` không xuất hiện confirm dialog; bản PDF dùng ảnh preview của video để bảo đảm minh chứng hiển thị ổn định. Lint failure không được tính là bug riêng cho 4 feature, nhưng được ghi nhận vì ảnh hưởng chất lượng source.

Các bug report chi tiết được gom trong `Bug_Report.md`, AI audit nằm trong `AI_Audit_Report.md`, AI critique nằm trong `AI_Critique.md`. Tất cả các Markdown report chính trong `reports/` đã được render lại thành PDF tương ứng trong cùng thư mục.

---

# FEATURE A: FR-02 - Login and Account Lockout

## 1.1 Domain Analysis

### SRS chính

- Người dùng nhập Email và Mật khẩu.
- Mỗi lần đăng nhập sai tăng bộ đếm đúng 1.
- Sai từ 3 lần liên tiếp thì khóa tài khoản 30 giây.
- Đăng nhập thành công trả JWT và reset số lần sai.
- Trường email trên form login phải dùng `type="email"`.

### Input variables

| ID | Biến | Domain hợp lệ | Domain không hợp lệ / edge |
|----|------|---------------|-----------------------------|
| V1 | `email` | Email tồn tại, đúng định dạng | Không tồn tại, rỗng, sai định dạng |
| V2 | `password` | Khớp mật khẩu user | Sai, rỗng |
| V3 | `login_attempts` | 0, 1, 2, 3 | Tăng sai, không reset |
| V4 | `locked_until` | `null` hoặc đã hết hạn | Còn hiệu lực; boundary 29s, 30s, 31s |

### Equivalence partitions

| EP-ID | Loại | Mô tả | Đại diện |
|-------|------|-------|----------|
| EP-FR02-01 | Valid | Email/password đúng | `admin@eshop.com / Admin123!` |
| EP-FR02-02 | Invalid | Email không tồn tại | `missing@example.com` |
| EP-FR02-03 | Invalid | Password sai | `Wrong123!` |
| EP-FR02-04 | State | Tài khoản chưa khóa sau 1-2 lần sai | attempts = 1, 2 |
| EP-FR02-05 | State | Tài khoản bị khóa sau 3 lần sai | attempts >= 3 |

## 1.2 Executed Test Cases

| TC-ID | Mô tả | Expected | Actual | Result | Bug |
|-------|-------|----------|--------|--------|-----|
| FR02-TC01 | Login đúng bằng user mới tạo | HTTP 200, có JWT | HTTP 200, token = true | PASS | - |
| FR02-TC02 | Login email không tồn tại | HTTP 401, lỗi generic | HTTP 401, `Invalid email or password` | PASS | - |
| FR02-TC03 | Form login dùng email input | `<input type="email">` | `Login.jsx` dùng `type="text"` và label `Username` | FAIL | BUG-FR02-003 |
| FR02-TC04 | Sai password lần 1 | `login_attempts = 1`, chưa khóa | HTTP 401, DB `login_attempts = 2`, `locked_until = null` | FAIL | BUG-FR02-001 |
| FR02-TC05 | Sai password lần 2 | `login_attempts = 2`, chưa khóa | HTTP 401, DB `login_attempts = 4`, có `locked_until` | FAIL | BUG-FR02-001 |
| FR02-TC06 | Login đúng sau 2 lần sai | Vẫn login được vì chưa đủ 3 lần sai | HTTP 403, tài khoản đã bị khóa | FAIL | BUG-FR02-001 |
| FR02-TC07 | Thời gian khóa | Khoảng 30 giây | Khoảng 180 giây | FAIL | BUG-FR02-002 |

## 1.3 Boundary Value Analysis

| Boundary | Expected | Actual từ test/source | Result |
|----------|----------|-----------------------|--------|
| attempts = 0 | Login đúng pass, attempts reset | HTTP 200 có token | PASS |
| attempts = 1 | Chưa khóa, attempts = 1 | attempts = 2 | FAIL |
| attempts = 2 | Chưa khóa | Đã tạo `locked_until` | FAIL |
| attempts = 3 | Bắt đầu khóa | Bị khóa sớm do counter tăng 2 | FAIL |
| lock time = 30s | Hết khóa quanh giây 30 | Source dùng `180000ms` | FAIL |
| email field type | HTML5 email validation | Source dùng `type="text"` | FAIL |

## 1.4 Metrics - FR-02

| Designed | Executed/Reviewed | Pass | Fail | Not run | Bugs |
|----------|-------------------|------|------|---------|------|
| 12 | 7 | 2 | 5 | 5 | 3 |

---

# FEATURE B: FR-07 - Shopping Cart

## 2.1 Domain Analysis

### SRS chính

- Giỏ hàng hiển thị sản phẩm, đơn giá, số lượng có nút `+/-`, thành tiền và thao tác.
- Thêm cùng sản phẩm phải tăng số lượng, không tạo dòng mới.
- Xóa sản phẩm phải có dialog xác nhận.
- Có nút tiếp tục mua sắm.
- Tổng tiền phải hiển thị nhãn `Tổng cộng`.
- Giỏ hàng trống phải có hình minh họa và thông báo rõ ràng.

### Input variables

| ID | Biến | Domain hợp lệ | Domain không hợp lệ / edge |
|----|------|---------------|-----------------------------|
| V1 | `product.id` | Product tồn tại | Trùng id, null |
| V2 | `quantity` | Số nguyên dương | 0, âm, text |
| V3 | `cart` | Empty, one row, many unique rows | Duplicate rows cùng product |
| V4 | remove action | Confirm rồi xóa | Xóa trực tiếp không confirm |

## 2.2 Executed Test Cases

| TC-ID | Mô tả | Expected | Actual | Result | Bug |
|-------|-------|----------|--------|--------|-----|
| FR07-TC01 | Giỏ hàng trống | Có thông báo + hình minh họa/icon | `Cart.jsx` chỉ có text và link, không có ảnh/icon | FAIL | BUG-FR07-005 |
| FR07-TC02 | Thêm sản phẩm mới | Có một dòng quantity = 1 | Source/API thêm được một dòng | PASS | - |
| FR07-TC03 | Thêm cùng sản phẩm 2 lần | Một dòng, quantity = 2 | API trả 2 dòng `id=1`, mỗi dòng `quantity=1` | FAIL | BUG-FR07-001 |
| FR07-TC04 | Cột số lượng | Có nút `+` và `-` | `Cart.jsx` chỉ render `{item.quantity}` | FAIL | BUG-FR07-002 |
| FR07-TC05 | Xóa sản phẩm | Hiển thị confirm dialog trước khi xóa | Button gọi `removeFromCart(index)` trực tiếp | FAIL | BUG-FR07-003 |
| FR07-TC06 | Tiếp tục mua sắm | Có link quay về trang chủ | Có link về `/` | PASS | - |
| FR07-TC07 | Nhãn tổng tiền | Hiển thị `Tổng cộng` | Hiển thị `Tổng tạm tính` | FAIL | BUG-FR07-004 |

## 2.3 Boundary Value Analysis

| Boundary | Expected | Actual | Result |
|----------|----------|--------|--------|
| cart count = 0 | Empty state có minh họa | Không có minh họa | FAIL |
| cart count = 1 | Một sản phẩm hiển thị đúng | Source/API hỗ trợ | PASS |
| same product count = 2 | Gộp thành quantity = 2 | Tạo duplicate row | FAIL |
| quantity = 1 | Giá dòng = price x 1 | Công thức đúng | PASS |
| quantity controls | Có thể tăng/giảm qua UI | Không có nút `+/-` | FAIL |

## 2.4 Metrics - FR-07

| Designed | Executed/Reviewed | Pass | Fail | Not run | Bugs |
|----------|-------------------|------|------|---------|------|
| 12 | 7 | 2 | 5 | 5 | 5 |

## 2.5 Video Evidence - FR-07 BUG-003

BUG-FR07-003 được ghi nhận bằng video thao tác UI: khi bấm `Xóa` trong giỏ hàng, sản phẩm bị xóa ngay mà không hiển thị confirm dialog.

<video controls src="./FR-07_bugs/BUG-003.mov" width="720"></video>

[Open video evidence: FR-07_bugs/BUG-003.mov](./FR-07_bugs/BUG-003.mov)

![BUG-FR07-003 preview](./FR-07_bugs/BUG-003-preview.png)

---

# FEATURE C: FR-16 - Product Import from CSV

## 3.1 Domain Analysis

### SRS chính

- Chỉ admin được import nhiều sản phẩm từ CSV.
- CSV phải có header `name,price,description,imageUrl,category_id`.
- Trường chứa dấu phẩy trong dấu nháy kép phải được hỗ trợ theo RFC 4180.
- `name` không rỗng.
- `price` là số dương.
- Nếu có lỗi ở bất kỳ dòng nào, toàn bộ import phải rollback.

### Input variables

| ID | Biến | Domain hợp lệ | Domain không hợp lệ / edge |
|----|------|---------------|-----------------------------|
| V1 | token role | `admin` | user thường, thiếu token |
| V2 | rows | Array không rỗng | Rỗng, không phải array |
| V3 | `name` | Không rỗng | Rỗng |
| V4 | `price` | Number > 0 | 0, âm, text |
| V5 | transaction | All-or-nothing | Partial insert |
| V6 | CSV field | Quoted comma đúng RFC 4180 | `split(",")` làm lệch cột |

## 3.2 Executed Test Cases

| TC-ID | Mô tả | Expected | Actual | Result | Bug |
|-------|-------|----------|--------|--------|-----|
| FR16-TC01 | Import không có token | HTTP 401 | HTTP 401 `Unauthorized` | PASS | - |
| FR16-TC02 | Import rows rỗng bằng admin | HTTP 400 | HTTP 400 `Không có dữ liệu để import` | PASS | - |
| FR16-TC03 | Admin import 1 product hợp lệ | HTTP 200, inserted = 1, DB có product | HTTP 200, inserted = 1, DB có product | PASS | - |
| FR16-TC04 | User thường gọi API import admin | HTTP 403, không insert | HTTP 200, inserted = 1, DB có product | FAIL | BUG-FR16-001 |
| FR16-TC05 | Batch có 1 dòng valid + 1 dòng thiếu name | Reject toàn batch, rollback | HTTP 200, inserted = 1/2, dòng valid vẫn vào DB | FAIL | BUG-FR16-002 |
| FR16-TC06 | Import price = -1000 | Reject, không insert | HTTP 200, inserted = 1, DB `price = -1000` | FAIL | BUG-FR16-003 |
| FR16-TC07 | CSV field chứa dấu phẩy trong dấu nháy kép | Parse đúng một field | Admin source dùng `line.split(",")`, sẽ tách sai cột | FAIL | BUG-FR16-004 |

## 3.3 Boundary Value Analysis

| Boundary | Expected | Actual | Result |
|----------|----------|--------|--------|
| rows = 0 | Reject | HTTP 400 | PASS |
| rows = 1 valid | Insert 1 dòng | HTTP 200, inserted 1 | PASS |
| rows = 2, dòng 2 invalid | Rollback toàn bộ | Insert 1 dòng valid | FAIL |
| price = 1 | Accept | Admin valid import pass với price dương | PASS |
| price = 0 | Reject | Source không có check `price > 0` | FAIL |
| price < 0 | Reject | Insert price âm | FAIL |

## 3.4 Metrics - FR-16

| Designed | Executed/Reviewed | Pass | Fail | Not run | Bugs |
|----------|-------------------|------|------|---------|------|
| 12 | 7 | 3 | 4 | 5 | 4 |

---

# FEATURE D: Mobile App - Product Listing/Search

## 4.1 Domain Analysis

### SRS áp dụng

Mobile listing/search được kiểm theo yêu cầu tương ứng của product listing:

- Hiển thị danh sách sản phẩm.
- Tìm kiếm theo tên sản phẩm.
- Có loading state.
- Không có kết quả phải hiển thị empty state.
- Ảnh sản phẩm phải giữ tỷ lệ chuẩn.
- API URL nên cấu hình theo môi trường để chạy được trên thiết bị khác nhau.

### Input variables

| ID | Biến | Domain hợp lệ | Domain không hợp lệ / edge |
|----|------|---------------|-----------------------------|
| V1 | API URL | Cấu hình đúng môi trường | Hard-code IP LAN cũ |
| V2 | search query | Chuỗi bình thường | Có `&`, `?`, khoảng trắng, ký tự đặc biệt |
| V3 | API response | Array có sản phẩm, array rỗng | HTML/error string |
| V4 | image mode | Giữ tỷ lệ ảnh | Stretch làm méo ảnh |

## 4.2 Executed Test Cases

| TC-ID | Mô tả | Expected | Actual | Result | Bug |
|-------|-------|----------|--------|--------|-----|
| MOB-TC01 | API danh sách sản phẩm | HTTP 200, array sản phẩm | HTTP 200, count >= 5 | PASS | - |
| MOB-TC02 | Search keyword bình thường | Trả product match tên | API search hoạt động với keyword cơ bản | PASS | - |
| MOB-TC03 | Search không có kết quả | API trả `[]` và UI có empty state | API trả `[]`, mobile UI không có `ListEmptyComponent` | FAIL | BUG-MOB-003 |
| MOB-TC04 | Search query có `&` | Query được encode nguyên chuỗi | `encoded_count=0`, `unencoded_count=1` do query bị cắt | FAIL | BUG-MOB-002 |
| MOB-TC05 | API URL mobile | Cấu hình theo môi trường | Hard-code `http://192.168.10.13:3000/api` | FAIL | BUG-MOB-001 |
| MOB-TC06 | Loading state | Có thông báo khi load | Có `loadingProducts` và text `Đang tải...` | PASS | - |
| MOB-TC07 | Ảnh sản phẩm | Giữ tỷ lệ chuẩn | `resizeMode="stretch"` ở listing/detail | FAIL | BUG-MOB-004 |

## 4.3 Boundary Value Analysis

| Boundary | Expected | Actual | Result |
|----------|----------|--------|--------|
| search = empty | Load toàn bộ danh sách | API trả danh sách | PASS |
| search = exact name | Có kết quả phù hợp | API trả product match | PASS |
| search = not found | Empty state rõ ràng | FlatList rỗng, không message | FAIL |
| search chứa `&` | Encode trước khi gọi API | Không encode | FAIL |
| products count = 0 | Hiển thị empty UI | Không có fallback UI | FAIL |

## 4.4 Metrics - Mobile

| Designed | Executed/Reviewed | Pass | Fail | Not run | Bugs |
|----------|-------------------|------|------|---------|------|
| 12 | 7 | 3 | 4 | 5 | 4 |

---

# 5. Tổng kết

| Feature | Designed | Executed/Reviewed | Pass | Fail | Not run | Bugs |
|---------|----------|-------------------|------|------|---------|------|
| FR-02 | 12 | 7 | 2 | 5 | 5 | 3 |
| FR-07 | 12 | 7 | 2 | 5 | 5 | 5 |
| FR-16 | 12 | 7 | 3 | 4 | 5 | 4 |
| Mobile listing/search | 12 | 7 | 3 | 4 | 5 | 4 |
| **Total** | **48** | **28** | **10** | **18** | **20** | **16** |

## 5.1 Các bug quan trọng nhất

1. **FR-16 user thường gọi được API import admin**: lỗi access control nghiêm trọng.
2. **FR-16 import không rollback**: sai yêu cầu all-or-nothing, làm dữ liệu không nhất quán.
3. **FR-02 login counter tăng 2**: gây khóa tài khoản sớm hơn SRS.
4. **FR-07 thêm trùng sản phẩm tạo duplicate row**: sai nghiệp vụ giỏ hàng cơ bản.
5. **Mobile search không encode query**: sai kết quả với keyword có ký tự đặc biệt.

## 5.2 Kết luận

Sau khi chạy API test thật và review source, 4 feature đều có lỗi sai so với SRS. Các lỗi backend/API có bằng chứng HTTP response và DB state; các lỗi UI/mobile có bằng chứng source line và ảnh evidence trong các thư mục bug tương ứng.
