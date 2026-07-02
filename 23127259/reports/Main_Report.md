# Main Testing Report - EShop Testing

**Họ và tên:** Nguyễn Tấn Thắng  
**Nhóm:** Nhóm 08  
**MSSV:** 23127259  
**Ngày lập:** 2026-07-03  

---

# FEATURE: FR-02 - LOGIN AND ACCOUNT LOCKOUT

## 1. Domain Testing - FR-02

**SUT:** Web Client Login + API `POST /api/login`

### Bước 1 - Phạm vi và SUT

**SRS FR-02:**
- User nhập Email và Password.
- Sai mật khẩu tăng counter đúng 1.
- Sai từ 3 lần trở lên bị khóa 30 giây.
- Login thành công trả JWT và reset counter.

**Files liên quan:**
- `backend/server.js`
- `backend/database.js`
- `frontend-web/src/pages/Login.jsx`

**Code review:** `server.js` tăng `login_attempts + 2` và khóa `180000ms` thay vì 30 giây.

### Bước 2 - Input Variables

| ID | Biến | Kiểu | Nguồn | Ràng buộc SRS |
|----|------|------|-------|---------------|
| V1 | email | String | Form/API | Email tồn tại, đúng định dạng |
| V2 | password | String | Form/API | Khớp tài khoản |
| V3 | login_attempts | Integer | DB | Tăng đúng 1 |
| V4 | locked_until | Datetime/null | DB | Khóa 30 giây |

### Bước 3 - Domains

| Biến | Valid Domain | Invalid Domain | Special |
|------|--------------|----------------|---------|
| email | `test@eshop.com` | unknown, rỗng, sai format | email đúng nhưng password sai |
| password | đúng | sai, rỗng | sai liên tiếp 1,2,3 lần |
| attempts | 0,1,2 trước khóa | tăng sai | 2/3 boundary |
| locked_until | null/hết hạn | còn hiệu lực | 29s,30s,31s |

### Bước 4 - Equivalence Partitions

| EP-ID | Loại | Mô tả | Giá trị đại diện |
|-------|------|-------|------------------|
| EP-L01 | Hợp lệ | Email/password đúng | `test@eshop.com` / `Test1234!` |
| EP-L02 | Không hợp lệ | Email không tồn tại | `none@eshop.com` |
| EP-L03 | Không hợp lệ | Password sai | `Wrong123!` |
| EP-L04 | Không hợp lệ | Account đang khóa | `locked_until > now` |
| EP-L05 | Hợp lệ | Account hết khóa | `locked_until < now` |

### Bước 5 - Constraints

| C-ID | Ràng buộc | Hành vi kỳ vọng |
|------|-----------|-----------------|
| C-01 | Sai password tăng counter | `attempts = old + 1` |
| C-02 | Sai 3 lần | Khóa 30 giây |
| C-03 | Login đúng | Reset counter và trả JWT |

### Bước 6 - Domain Test Cases

| TC-ID | Mô tả | Input | Expected | Actual | Result | Bug |
|-------|-------|-------|----------|--------|--------|-----|
| DT-FR02-01 | Login hợp lệ | correct email/password | HTTP 200, token | PASS evidence cũ | PASS | - |
| DT-FR02-02 | Email không tồn tại | unknown email | HTTP 401 | Not run | NOT RUN | - |
| DT-FR02-03 | Sai password lần 1 | wrong password | attempts +1 | attempts +2 | FAIL | BUG-FR02-001 |
| DT-FR02-04 | Sai 2 lần rồi login đúng | 2 wrong + correct | Chưa khóa | Bị khóa | FAIL | BUG-FR02-001 |
| DT-FR02-05 | Sai lần 3 | 3 wrong | Khóa 30s | Khóa sớm | FAIL | BUG-FR02-001 |
| DT-FR02-06 | Login khi khóa | correct password | HTTP 403 | HTTP 403 | PASS | - |

## 2. Boundary Value Analysis - FR-02

| TC-ID | Boundary | Input | Expected | Actual | Result | Bug |
|-------|----------|-------|----------|--------|--------|-----|
| BV-FR02-01 | attempts = 0 | Login đúng | Success | PASS | PASS | - |
| BV-FR02-02 | attempts = 1 | Sai 1 lần | counter = 1 | counter = 2 | FAIL | BUG-FR02-001 |
| BV-FR02-03 | attempts = 2 | Sai 2 lần | Chưa khóa | Đã khóa | FAIL | BUG-FR02-001 |
| BV-FR02-04 | attempts = 3 | Sai lần 3 | Khóa | Khóa sớm | FAIL | BUG-FR02-001 |
| BV-FR02-05 | lock = 30s | Login tại giây 30 | Cho login | Code khóa 180s | FAIL | BUG-FR02-002 |

## 3. Test Execution - FR-02

| Metric | Count |
|--------|------:|
| Designed | 15 |
| Executed/Reviewed | 7 |
| Pass | 2 |
| Fail | 5 |
| Not run | 8 |
| Bugs | 2 |

---

# FEATURE: FR-07 - SHOPPING CART

## 1. Domain Testing - FR-07

**SUT:** Web Cart page + `CartContext.jsx`

**SRS FR-07:**
- Hiển thị sản phẩm, đơn giá, số lượng có `+/-`, thành tiền, thao tác.
- Thêm cùng sản phẩm tăng số lượng, không tạo dòng mới.
- Xóa có dialog xác nhận.
- Có nút tiếp tục mua sắm.
- Tổng tiền nhãn `Tổng cộng`.
- Cart trống có hình minh họa.

**Files liên quan:** `frontend-web/src/context/CartContext.jsx`, `frontend-web/src/pages/Cart.jsx`.

### Input Variables

| ID | Biến | Kiểu | Ràng buộc |
|----|------|------|-----------|
| V1 | product.id | Integer | Nhận diện sản phẩm trùng |
| V2 | quantity | Integer | > 0 |
| V3 | cart | Array | Không có duplicate row |
| V4 | remove action | UI event | Phải confirm trước khi xóa |

### Domains and EP

| EP-ID | Loại | Mô tả | Đại diện |
|-------|------|-------|----------|
| EP-CART-01 | Hợp lệ | Empty cart | `[]` |
| EP-CART-02 | Hợp lệ | One product | iPhone x1 |
| EP-CART-03 | Hợp lệ | Same product twice | iPhone x2 một dòng |
| EP-CART-04 | Không hợp lệ | Same product tạo 2 dòng | iPhone row + iPhone row |
| EP-CART-05 | Không hợp lệ | Quantity không chỉnh được | plain text |

### Domain Test Cases

| TC-ID | Mô tả | Expected | Actual | Result | Bug |
|-------|-------|----------|--------|--------|-----|
| DT-FR07-01 | Cart trống | Message + hình minh họa | Không có hình | FAIL | BUG-FR07-005 |
| DT-FR07-02 | Add new product | One row qty 1 | PASS source | PASS | - |
| DT-FR07-03 | Add duplicate product | Tăng quantity | Tạo dòng mới | FAIL | BUG-FR07-001 |
| DT-FR07-04 | Quantity controls | Có `+/-` | Plain text | FAIL | BUG-FR07-002 |
| DT-FR07-05 | Delete item | Có confirm | Xóa trực tiếp | FAIL | BUG-FR07-003 |
| DT-FR07-06 | Continue shopping | Về home | Link `/` | PASS | - |
| DT-FR07-07 | Total label | `Tổng cộng` | `Tổng tạm tính` | FAIL | BUG-FR07-004 |

## 2. Boundary Value Analysis - FR-07

| TC-ID | Boundary | Input | Expected | Actual | Result | Bug |
|-------|----------|-------|----------|--------|--------|-----|
| BV-FR07-01 | cart count = 0 | Empty | Empty state + image | No image | FAIL | BUG-FR07-005 |
| BV-FR07-02 | cart count = 1 | One item | One row | PASS | PASS | - |
| BV-FR07-03 | same product = 2 | Add twice | One row qty 2 | Duplicate row | FAIL | BUG-FR07-001 |
| BV-FR07-04 | quantity = -1 | Invalid qty | Reject/normalize | No validation | FAIL | BUG-FR07-002 |
| BV-FR07-05 | quantity = 0 | Invalid qty | Reject/normalize | No validation | FAIL | BUG-FR07-002 |
| BV-FR07-06 | quantity = 1 | Valid qty | Accept | PASS | PASS | - |

## 3. Test Execution - FR-07

| Metric | Count |
|--------|------:|
| Designed | 18 |
| Executed/Reviewed | 12 |
| Pass | 4 |
| Fail | 8 |
| Not run | 6 |
| Bugs | 5 |

---

# FEATURE: FR-16 - PRODUCT IMPORT FROM CSV

## 1. Domain Testing - FR-16

**SUT:** Admin import API `POST /api/admin/import-products`

**SRS FR-16:**
- Chỉ admin được import.
- CSV header đúng: `name,price,description,imageUrl,category_id`.
- `name` không rỗng.
- `price` > 0.
- Có lỗi bất kỳ dòng nào thì rollback toàn bộ.

### Variables and Domains

| Biến | Valid Domain | Invalid Domain | Boundary |
|------|--------------|----------------|----------|
| token.role | admin | user/no token | user token |
| rows | 1+ valid rows | empty array | 0,1,many |
| name | non-empty | empty/whitespace | length 0/1 |
| price | > 0 | 0, negative, text | -1,0,1 |

### Domain Test Cases

| TC-ID | Mô tả | Expected | Actual | Result | Bug |
|-------|-------|----------|--------|--------|-----|
| DT-FR16-01 | Admin valid row | Insert 1 | Not run | NOT RUN | - |
| DT-FR16-02 | User thường import | HTTP 403 | HTTP 200 | FAIL | BUG-FR16-001 |
| DT-FR16-03 | No token | HTTP 401 | Not run | NOT RUN | - |
| DT-FR16-04 | Missing name | Reject + rollback | Partial insert | FAIL | BUG-FR16-002 |
| DT-FR16-05 | Negative price | Reject | Inserted | FAIL | BUG-FR16-003 |
| DT-FR16-06 | Mixed invalid batch | Insert 0 | Inserted 2/3 | FAIL | BUG-FR16-002 |

## 2. Boundary Value Analysis - FR-16

| TC-ID | Boundary | Input | Expected | Actual | Result | Bug |
|-------|----------|-------|----------|--------|--------|-----|
| BV-FR16-01 | rows = 0 | empty array | HTTP 400 | Not run | NOT RUN | - |
| BV-FR16-02 | rows = 1 | one valid row | Insert | Not run | NOT RUN | - |
| BV-FR16-03 | name length = 0 | `""` | Reject rollback | Rollback missing | FAIL | BUG-FR16-002 |
| BV-FR16-04 | name length = 1 | `"A"` | Accept | Not run | NOT RUN | - |
| BV-FR16-05 | price = -1 | negative | Reject | Inserted | FAIL | BUG-FR16-003 |
| BV-FR16-06 | price = 0 | zero | Reject | Not run | NOT RUN | - |
| BV-FR16-07 | price = 1 | min valid | Accept | Not run | NOT RUN | - |

## 3. Test Execution - FR-16

| Metric | Count |
|--------|------:|
| Designed | 15 |
| Executed/Reviewed | 4 |
| Pass | 0 |
| Fail | 4 |
| Not run | 11 |
| Bugs | 3 |

---

# FEATURE: MOBILE PRODUCT LISTING/SEARCH

## 1. Domain Testing - Mobile Product listing/search

**SUT:** `frontend-mobile/App.js`, mobile home product list/search.

**Rules:**
- Hiển thị product list với ảnh, tên, giá.
- Search theo tên sản phẩm.
- Có loading state.
- Có empty state khi không có kết quả.
- Query search encode an toàn.
- API URL cấu hình theo môi trường.

### Variables and Domains

| Biến | Valid Domain | Invalid Domain | Boundary |
|------|--------------|----------------|----------|
| API_URL | reachable backend | hard-code IP sai mạng | device/emulator |
| search | keyword thường | special chars chưa encode | length 0/1/long |
| products | 1/many | 0 result không message | count 0/1/many |
| image | giữ aspect ratio | stretch méo ảnh | wide/tall image |

### Domain Test Cases

| TC-ID | Mô tả | Expected | Actual | Result | Bug |
|-------|-------|----------|--------|--------|-----|
| DT-MOB-01 | Load product list | Hiển thị list | FlatList | PASS | - |
| DT-MOB-02 | Loading state | `Đang tải...` | Có loading text | PASS | - |
| DT-MOB-03 | Search keyword | Matching products | API search | PASS | - |
| DT-MOB-04 | No result | Empty state | Missing | FAIL | BUG-MOB-003 |
| DT-MOB-05 | Special chars query | Encoded | Direct interpolation | FAIL | BUG-MOB-002 |
| DT-MOB-06 | Different device IP | Configurable | Hard-coded IP | FAIL | BUG-MOB-001 |
| DT-MOB-07 | Image ratio | Preserve ratio | `stretch` | FAIL | BUG-MOB-004 |

## 2. Boundary Value Analysis - Mobile

| TC-ID | Boundary | Input | Expected | Actual | Result | Bug |
|-------|----------|-------|----------|--------|--------|-----|
| BV-MOB-01 | keyword length = 0 | empty | all/current products | Not run | NOT RUN | - |
| BV-MOB-02 | keyword length = 1 | `i` | request ok | Not run | NOT RUN | - |
| BV-MOB-03 | long keyword | 255 chars | responsive | Not run | NOT RUN | - |
| BV-MOB-04 | special chars | `a&b=<x>` | encode | Not encoded | FAIL | BUG-MOB-002 |
| BV-MOB-05 | result count = 0 | no match | empty state | Missing | FAIL | BUG-MOB-003 |
| BV-MOB-06 | result count = 1 | exact match | one product | Not run | NOT RUN | - |

## 3. Test Execution - Mobile

| Metric | Count |
|--------|------:|
| Designed | 16 |
| Executed/Reviewed | 10 |
| Pass | 4 |
| Fail | 6 |
| Not run | 6 |
| Bugs | 4 |

---

# AI Gap Analysis

AI giúp tạo nhanh checklist Domain Testing và BVA, nhưng dễ bỏ sót lỗi implementation nếu không đọc source. Ví dụ, AI có thể nêu yêu cầu thêm trùng sản phẩm phải tăng quantity, nhưng chỉ khi review `CartContext.jsx` mới thấy code luôn append item. Với FR-16, nếu không nhắc "rollback toàn bộ batch", AI có thể chỉ kiểm tra từng row riêng lẻ. Với Mobile, các lỗi như hard-code API URL, thiếu empty state, query không encode đều chỉ rõ khi đọc `frontend-mobile/App.js`.

# Test Summary

| Feature | Designed | Executed/Reviewed | Passed | Failed | Not Run | Bugs |
|---------|---------:|------------------:|-------:|-------:|--------:|-----:|
| FR-02 Login and account lockout | 15 | 7 | 2 | 5 | 8 | 2 |
| FR-07 Shopping cart | 18 | 12 | 4 | 8 | 6 | 5 |
| FR-16 Product import from CSV | 15 | 4 | 0 | 4 | 11 | 3 |
| Mobile Product listing/search | 16 | 10 | 4 | 6 | 6 | 4 |
| **Total** | **64** | **33** | **10** | **23** | **31** | **14** |
