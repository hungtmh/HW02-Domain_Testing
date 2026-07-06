<!-- File: FR-04_TestReport.md -->

# BÁO CÁO KIỂM THỬ: FR-04 – Quản lý Hồ sơ Cá nhân (User Profile Management)

> **API mục tiêu:** `PUT /api/users/me`  
> **Phương pháp:** Domain Testing + Boundary Value Analysis (BVA)  
> **Trọng tâm:** Trường `phone` – phân tích khoảng hợp lệ, biên, và bypass frontend

---

## Bối cảnh Phân tích (Context)

### Phát hiện bất đồng nhất (Frontend vs Backend)

| Tầng | Hành vi |
|------|---------|
| **Frontend** (`Profile.jsx`, dòng 43) | Kiểm tra regex `/^[1-9][0-9]{8,9}$/` trước khi gọi API. Nếu sai → hiện alert, **không gửi request**. |
| **Backend** (`server.js`, dòng 118–135) | **KHÔNG** có bất kỳ validation nào cho `phone`. Nhận giá trị bất kỳ và ghi thẳng vào SQLite. |
| **Database** (`database.js`, dòng 60) | Cột `phone TEXT` – không có ràng buộc `NOT NULL`, `CHECK`, hoặc độ dài. |

> **Lỗ hổng nghiêm trọng (Critical Gap):** Bất kỳ client nào bypass frontend (Postman, curl, script) đều có thể ghi giá trị `phone` tuỳ ý vào database mà không bị từ chối. Đây là lỗi thiếu **server-side validation**.

---

## BƯỚC 1: Phân tích Miền Giá Trị (Domain Testing Analysis)

### 1.1 Xác định các biến đầu vào

API `PUT /api/users/me` nhận body JSON:

| Biến | Kiểu dữ liệu | Ghi chú |
|------|-------------|---------|
| `name` | `TEXT` | Bắt buộc (`required`) ở form frontend |
| `phone` | `TEXT` | Validation chỉ ở frontend |
| `shipping_address` | `TEXT` | Không có ràng buộc |
| `role` | `TEXT` | Nếu có → backend sẽ cập nhật role (lỗ hổng leo thang đặc quyền!) |

> **Phạm vi phân tích:** Tập trung vào `phone`. Các trường `name` và `shipping_address` không có ràng buộc rõ ràng nên sử dụng giá trị hợp lệ cố định trong các test case.

### 1.2 Phân tích Regex Frontend: `/^[1-9][0-9]{8,9}$/`

| Thành phần Regex | Ý nghĩa |
|-----------------|---------|
| `^` | Bắt đầu chuỗi |
| `[1-9]` | Ký tự đầu tiên: chữ số từ 1 đến 9 (không được là 0) |
| `[0-9]{8,9}` | Tiếp theo: 8 hoặc 9 chữ số bất kỳ (0–9) |
| `$` | Kết thúc chuỗi |

**→ Tổng độ dài hợp lệ:** 9 ký tự (1 + 8) hoặc 10 ký tự (1 + 9)

### 1.3 Phân hoạch tương đương (Equivalence Partitioning)

#### ✅ Lớp Hợp Lệ (Valid Equivalence Classes)

| ID Lớp | Mô tả | Ví dụ |
|--------|-------|-------|
| **VEC-1** | Chuỗi 9 ký tự số, bắt đầu bằng [1-9] | `912345678` |
| **VEC-2** | Chuỗi 10 ký tự số, bắt đầu bằng [1-9] | `9123456789` |

#### ❌ Lớp Không Hợp Lệ (Invalid Equivalence Classes)

| ID Lớp | Mô tả | Ví dụ |
|--------|-------|-------|
| **IEC-1** | Chuỗi rỗng (empty string) | `""` |
| **IEC-2** | Null / undefined | `null` |
| **IEC-3** | Độ dài quá ngắn (< 9 ký tự) | `12345678` (8 ký tự) |
| **IEC-4** | Độ dài quá dài (> 10 ký tự) | `12345678901` (11 ký tự) |
| **IEC-5** | Bắt đầu bằng `0` (không hợp lệ theo regex) | `0912345678` |
| **IEC-6** | Chứa chữ cái | `abc123456` |
| **IEC-7** | Chứa ký tự đặc biệt | `+84912345678`, `091-234-5678` |
| **IEC-8** | Chỉ là khoảng trắng | `"         "` |
| **IEC-9** | Payload SQL Injection | `'; DROP TABLE users; --` |
| **IEC-10** | Payload XSS | `<script>alert(1)</script>` |
| **IEC-11** | Số âm hoặc bắt đầu bằng dấu trừ | `-912345678` |
| **IEC-12** | Số dấu phẩy động | `9.123456789` |
| **IEC-13** | Chuỗi rất dài (stress test) | chuỗi 1000 ký tự |

---

## BƯỚC 2: Phân tích Giá Trị Biên (BVA)

### 2.1 Biên về Độ Dài (Length Boundaries)

Điều kiện hợp lệ: `length ∈ [9, 10]`

| Loại Biên | Giá trị độ dài | Dữ liệu ví dụ | Kỳ vọng (Frontend) | Kỳ vọng (Backend trực tiếp) |
|-----------|---------------|--------------|-------------------|-----------------------------|
| **Dưới biên dưới** (< 9) | 8 ký tự | `91234567` | ❌ Reject (alert) | ✅ Ghi DB thành công |
| **Tại biên dưới** (= 9) | 9 ký tự | `912345678` | ✅ Accept | ✅ Ghi DB thành công |
| **Trên biên dưới** (> 9, hợp lệ) | 10 ký tự | `9123456789` | ✅ Accept | ✅ Ghi DB thành công |
| **Tại biên trên** (= 10) | 10 ký tự | `9123456789` | ✅ Accept | ✅ Ghi DB thành công |
| **Trên biên trên** (> 10) | 11 ký tự | `91234567890` | ❌ Reject (alert) | ✅ Ghi DB thành công |

### 2.2 Biên về Ký Tự Đầu Tiên (First Character Boundaries)

Ký tự đầu hợp lệ: `[1-9]` (tức là giá trị số nguyên từ 1 đến 9)

| Loại Biên | Ký tự đầu | Dữ liệu ví dụ | Kỳ vọng (Frontend) | Kỳ vọng (Backend trực tiếp) |
|-----------|----------|--------------|-------------------|-----------------------------|
| **Dưới biên dưới** | `0` | `012345678` | ❌ Reject | ✅ Ghi DB thành công |
| **Tại biên dưới** | `1` | `123456789` | ✅ Accept | ✅ Ghi DB thành công |
| **Trong khoảng** | `5` | `512345678` | ✅ Accept | ✅ Ghi DB thành công |
| **Tại biên trên** | `9` | `912345678` | ✅ Accept | ✅ Ghi DB thành công |
| **Trên biên trên** | chữ cái / ký tự đặc biệt | `a12345678` | ❌ Reject | ✅ Ghi DB thành công |

### 2.3 Tóm tắt Biên Quan Trọng

```
Độ dài: 8 | [9 ............ 10] | 11
              ↑ biên dưới       ↑ biên trên
Ký tự đầu: 0 | [1 ........... 9] | (chữ/ký tự)
               ↑ biên dưới      ↑ biên trên
```

---

## BƯỚC 3: Bảng Test Case

> **Chú thích cột "Kết quả mong đợi":**
> - **(FE)** = Kiểm tra qua giao diện web (có frontend validation)
> - **(API)** = Gọi thẳng API bằng Postman/curl (bypass frontend)
> - **"Ghi DB"** = Backend trả 200, phone được lưu vào database

### Nhóm 1: Test Case Domain Testing – Phân hoạch Tương Đương

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào `phone` | Kết quả mong đợi (Expected Output) | Loại |
|-------------|---------------------|------------------------|-------------------------------------|------|
| **TC-D01** | Đại diện lớp hợp lệ VEC-1: 9 chữ số, đầu [1-9] | `912345678` | (FE) Accept, (API) `200 {"message":"Profile updated"}`, phone được lưu | Valid |
| **TC-D02** | Đại diện lớp hợp lệ VEC-2: 10 chữ số, đầu [1-9] | `9123456789` | (FE) Accept, (API) `200 {"message":"Profile updated"}`, phone được lưu | Valid |
| **TC-D03** | Đại diện IEC-1: chuỗi rỗng | `""` | (FE) Reject – alert lỗi validation; (API) `200` – **LỖI: ghi `""` vào DB** | Invalid |
| **TC-D04** | Đại diện IEC-2: giá trị null | `null` | (FE) Reject; (API) `200` – **LỖI: ghi `null` vào DB** | Invalid |
| **TC-D05** | Đại diện IEC-3: chuỗi quá ngắn (8 ký tự) | `91234567` | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-D06** | Đại diện IEC-4: chuỗi quá dài (11 ký tự) | `91234567890` | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-D07** | Đại diện IEC-5: bắt đầu bằng `0` | `0912345678` | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-D08** | Đại diện IEC-6: chứa chữ cái | `abc1234567` | (FE) Reject – alert; (API) `200` – **LỖI: ghi chuỗi text vào DB** | Invalid |
| **TC-D09** | Đại diện IEC-7: có ký tự `+` (format quốc tế) | `+84912345678` | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-D10** | Đại diện IEC-8: chỉ là khoảng trắng | `"         "` (9 spaces) | (FE) Reject – alert; (API) `200` – **LỖI: ghi spaces vào DB** | Invalid |

### Nhóm 2: Test Case BVA – Biên Độ Dài

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào `phone` | Độ dài | Kết quả mong đợi (Expected Output) | Loại |
|-------------|---------------------|------------------------|--------|-------------------------------------|------|
| **TC-B01** | Dưới biên dưới: 7 ký tự | `9123456` | 7 | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-B02** | Biên dưới (min - 1): 8 ký tự | `91234567` | 8 | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-B03** | **Tại biên dưới (min): 9 ký tự** | `912345678` | 9 | (FE) Accept; (API) `200 {"message":"Profile updated"}` | **Valid** |
| **TC-B04** | Trên biên dưới (min + 1): 10 ký tự | `9123456789` | 10 | (FE) Accept; (API) `200 {"message":"Profile updated"}` | **Valid** |
| **TC-B05** | **Tại biên trên (max): 10 ký tự** | `9123456789` | 10 | (FE) Accept; (API) `200 {"message":"Profile updated"}` | **Valid** |
| **TC-B06** | Trên biên trên (max + 1): 11 ký tự | `91234567890` | 11 | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-B07** | Trên biên trên + 1: 12 ký tự | `912345678901` | 12 | (FE) Reject – alert; (API) `200` – **LỖI: ghi vào DB** | Invalid |

### Nhóm 3: Test Case BVA – Biên Ký Tự Đầu Tiên

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào `phone` | Ký tự đầu | Kết quả mong đợi (Expected Output) | Loại |
|-------------|---------------------|------------------------|-----------|------------------------------------|------|
| **TC-C01** | Ký tự đầu = `0` (dưới biên [1-9]) | `012345678` | `0` | (FE) Reject – alert "không hợp lệ"; (API) `200` – **LỖI: ghi vào DB** | Invalid |
| **TC-C02** | **Tại biên dưới: ký tự đầu = `1`** | `123456789` | `1` | (FE) Accept; (API) `200` – Ghi DB đúng | **Valid** |
| **TC-C03** | Giữa khoảng: ký tự đầu = `5` | `512345678` | `5` | (FE) Accept; (API) `200` – Ghi DB đúng | Valid |
| **TC-C04** | **Tại biên trên: ký tự đầu = `9`** | `912345678` | `9` | (FE) Accept; (API) `200` – Ghi DB đúng | **Valid** |
| **TC-C05** | Vượt biên trên: ký tự đầu là chữ thường | `a12345678` | `a` | (FE) Reject; (API) `200` – **LỖI: ghi text vào DB** | Invalid |
| **TC-C06** | Vượt biên trên: ký tự đầu là chữ hoa | `A12345678` | `A` | (FE) Reject; (API) `200` – **LỖI: ghi text vào DB** | Invalid |
| **TC-C07** | Ký tự đầu là ký tự đặc biệt `+` | `+12345678` | `+` | (FE) Reject; (API) `200` – **LỖI: ghi text vào DB** | Invalid |

### Nhóm 4: Test Case Bypass Frontend – Tấn công API Trực Tiếp

> Các test case này phải thực hiện bằng **Postman / curl**, **không dùng trình duyệt**.  
> Cần có JWT token hợp lệ: đăng nhập với `test@eshop.com` / `Test1234!` trước.

**Cách lấy token:**
```
POST http://localhost:3000/api/login
Body: { "email": "test@eshop.com", "password": "Test1234!" }
→ Lấy giá trị trường "token" từ response
```

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (curl/Postman body) | Kết quả mong đợi (Expected Output) | Loại |
|-------------|---------------------|--------------------------------------|--------------------------------------|------|
| **TC-API01** | Bypass FE: gửi phone rỗng trực tiếp | `{"name":"Test","phone":"","shipping_address":"HN"}` | **LỖI BẢO MẬT:** Server trả `200`, DB ghi `phone = ""` | Invalid |
| **TC-API02** | Bypass FE: gửi phone 8 ký tự | `{"name":"Test","phone":"91234567","shipping_address":"HN"}` | **LỖI BẢO MẬT:** Server trả `200`, DB ghi số 8 chữ số | Invalid |
| **TC-API03** | Bypass FE: gửi phone 11 ký tự | `{"name":"Test","phone":"91234567890","shipping_address":"HN"}` | **LỖI BẢO MẬT:** Server trả `200`, DB ghi số 11 chữ số | Invalid |
| **TC-API04** | Bypass FE: gửi phone bắt đầu bằng `0` | `{"name":"Test","phone":"0912345678","shipping_address":"HN"}` | **LỖI BẢO MẬT:** Server trả `200`, DB ghi `phone = "0912345678"` | Invalid |
| **TC-API05** | Bypass FE: gửi chuỗi chữ cái | `{"name":"Test","phone":"not-a-phone","shipping_address":"HN"}` | **LỖI BẢO MẬT:** Server trả `200`, DB ghi chuỗi text | Invalid |
| **TC-API06** | Bypass FE: SQL Injection vào phone | `{"name":"Test","phone":"'; DROP TABLE users; --","shipping_address":"HN"}` | Server trả `200`, DB ghi nguyên chuỗi (SQLite parameterized – không drop table, nhưng vẫn lưu payload!) | Invalid |
| **TC-API07** | Bypass FE: XSS payload vào phone | `{"name":"Test","phone":"<script>alert(1)</script>","shipping_address":"HN"}` | **LỖI:** Server trả `200`, DB lưu XSS payload. Nếu admin UI hiển thị phone không encode → XSS! | Invalid |
| **TC-API08** | Bypass FE: gửi null | `{"name":"Test","phone":null,"shipping_address":"HN"}` | **LỖI BẢO MẬT:** Server trả `200`, DB ghi `NULL` | Invalid |
| **TC-API09** | Bypass FE: chuỗi siêu dài (stress) | `{"name":"Test","phone":"9" + "1".repeat(999),"shipping_address":"HN"}` | **LỖI:** Server trả `200`, DB lưu chuỗi 1000 ký tự (SQLite không giới hạn TEXT) | Invalid |
| **TC-API10** | Bypass FE: leo thang đặc quyền (role injection) | `{"name":"Test","phone":"912345678","shipping_address":"HN","role":"admin"}` | **LỖI NGHIÊM TRỌNG:** Server trả `200`, user bị nâng cấp thành `admin`! | Invalid |

### Nhóm 5: Test Case Đặc Biệt – Edge Cases

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào `phone` | Kết quả mong đợi (Expected Output) | Loại |
|-------------|---------------------|------------------------|--------------------------------------|------|
| **TC-E01** | Phone chứa dấu gạch ngang (format phổ biến) | `091-234-567` | (FE) Reject; (API) `200` – Ghi vào DB | Invalid |
| **TC-E02** | Phone chứa dấu chấm | `091.234.567` | (FE) Reject; (API) `200` – Ghi vào DB | Invalid |
| **TC-E03** | Chuỗi Unicode/emoji | `📱12345678` | (FE) Reject; (API) `200` – Ghi vào DB | Invalid |
| **TC-E04** | Chuỗi chỉ khoảng trắng (10 spaces) | `"          "` | (FE) Reject; (API) `200` – Ghi spaces vào DB | Invalid |
| **TC-E05** | Phone hợp lệ nhưng `name` rỗng | `name=""`, `phone="912345678"` | (FE) Reject (trường name required); (API) `200` – **LỖI: ghi name="" vào DB** | Invalid |
| **TC-E06** | Không truyền trường `phone` (omit) | Body không có key `phone` | (API) `200` – Server ghi `phone = undefined = NULL` vào DB. Phone cũ bị xóa! | Invalid |

---

## Tóm tắt Rủi ro & Khuyến nghị

### Rủi ro phát hiện được

| Mức độ | Vấn đề | Mô tả |
|--------|--------|-------|
| 🔴 **CRITICAL** | Không có server-side validation cho `phone` | Bất kỳ giá trị nào cũng được ghi vào DB |
| 🔴 **CRITICAL** | `role` escalation qua PUT /api/users/me | Gửi `role: "admin"` → thành admin ngay lập tức |
| 🟠 **HIGH** | XSS stored qua trường `phone` | Payload JS được lưu và hiển thị không encode |
| 🟡 **MEDIUM** | Không validate `name` (empty string accepted) | Tên người dùng có thể là chuỗi rỗng |
| 🟡 **MEDIUM** | Phone cũ bị xóa khi không gửi field | Thiếu field = ghi NULL, không giữ giá trị cũ |

### Khuyến nghị

```javascript
// Thêm vào server.js, trong handler PUT /api/users/me:
const phoneRegex = /^[1-9][0-9]{8,9}$/;
if (phone !== undefined && !phoneRegex.test(phone)) {
  return res.status(400).json({ error: "Số điện thoại không hợp lệ" });
}
// Loại bỏ khả năng cập nhật role qua endpoint này
const { name, shipping_address, phone } = req.body; // Không destructure 'role'
```

---

*Báo cáo được tạo bởi: Antigravity AI (Google DeepMind) | Ngày: 2026-07-06*
