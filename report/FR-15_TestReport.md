&lt;!-- File: FR-15_TestReport.md --&gt;

# BÁO CÁO KIỂM THỬ: FR-15 — Quản lý Sản phẩm (Tạo / Cập nhật qua Admin Panel)

**Phiên bản:** 1.0  
**Ngày:** 2026-07-06  
**Người thực hiện:** Antigravity QA Agent (Claude Sonnet — Thinking Mode)  
**Phạm vi:** `POST /api/products` · `PUT /api/products/:id` · Form Admin (`App.jsx`)

---

## Tổng quan về SUT (System Under Test)

### Frontend — `frontend-admin/src/App.jsx`

Form thêm/sửa sản phẩm (dòng 483–566) có các trường sau:

| Trường | Loại input HTML | Ràng buộc Frontend | Ghi chú |
|---|---|---|---|
| `name` | `input type="text"` | `required` (HTML5) | Chỉ kiểm tra rỗng qua thuộc tính `required` |
| `price` | `input type="number"` | **Không có** `min`, `max`, không `required` | Giá trị lưu thẳng dạng **string** (`e.target.value`) vào `productForm` |
| `imageUrl` | `input type="text"` | Không có | Tùy chọn |
| `description` | `textarea` | Không có | Tùy chọn |
| `category_id` | `select` | Chọn từ danh sách | Không ép kiểu |

**Lỗ hổng thiết kế quan trọng (dòng 505–507):**

price được lưu thẳng dưới dạng string: `setProductForm({ ...productForm, price: e.target.value })`  
→ `productForm.price` là **string**, không phải number. Khi gửi qua `axios.post`, giá trị được truyền thẳng dưới dạng string JSON.

### Backend — `backend/server.js` (dòng 167–177)

```js
app.post("/api/products", (req, res) => {
  const { name, price, description, imageUrl, category_id } = req.body;
  db.run(
    "INSERT INTO products (name, price, description, imageUrl, category_id) VALUES (?, ?, ?, ?, ?)",
    [name, price, description, imageUrl, category_id],   // KHÔNG validate kiểu
    ...
  );
});
```
**Không có bất kỳ validation nào** cho `price` (âm, rỗng, chuỗi ký tự, số quá lớn).

### Database Schema — `backend/database.js` (dòng 64–71)

```sql
CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    price       INTEGER,      -- khai báo INTEGER nhưng SQLite là dynamically typed
    description TEXT,
    imageUrl    TEXT,
    category_id INTEGER
);
```

**SQLite Type Affinity:** Dù khai báo `INTEGER`, SQLite lưu bất kỳ giá trị nào được truyền vào — kể cả chuỗi ký tự — mà **không báo lỗi**. Điều này dẫn đến dữ liệu bẩn trong database.

---

## BƯỚC 1: Phân tích Miền giá trị (Domain Testing Analysis)

### 1.1 Biến đầu vào và trạng thái hệ thống

| # | Biến | Kiểu kỳ vọng | Nguồn |
|---|---|---|---|
| 1 | `name` | string, bắt buộc, không rỗng | `req.body.name` |
| 2 | `price` | integer ≥ 0 | `req.body.price` |
| 3 | `description` | string, tùy chọn | `req.body.description` |
| 4 | `imageUrl` | string URL, tùy chọn | `req.body.imageUrl` |
| 5 | `category_id` | integer, FK đến bảng `categories` | `req.body.category_id` |

### 1.2 Phân tích miền cho `name` (Trường bắt buộc)

**Miền hợp lệ (Valid Domain):**
- `V_Name_1`: Chuỗi không rỗng, độ dài 1–255 ký tự → Ví dụ: `"iPhone 15 Pro Max"`
- `V_Name_2`: Chuỗi có ký tự đặc biệt nhưng không rỗng → Ví dụ: `"Sản phẩm #1 (mới)"`

**Miền không hợp lệ (Invalid Domain):**
- `I_Name_1`: Chuỗi rỗng `""` — HTML5 `required` chặn tại UI, nhưng API không chặn
- `I_Name_2`: Chỉ có khoảng trắng `"   "` — HTML5 `required` **KHÔNG chặn** được
- `I_Name_3`: `null` / `undefined` — gửi trực tiếp qua API
- `I_Name_4`: Chuỗi cực dài (> 10,000 ký tự) — SQLite TEXT không có giới hạn cứng

### 1.3 Phân tích miền cho `price` (Trường trọng tâm)

Dựa trên ngữ nghĩa nghiệp vụ: **Giá sản phẩm phải là số nguyên không âm (≥ 0)**.

| Lớp tương đương | Mô tả | Đại diện | Hợp lệ? |
|---|---|---|---|
| `EC_P_1` | Số nguyên dương bình thường | `100000` | ✅ Valid |
| `EC_P_2` | Số nguyên = 0 (giá miễn phí) | `0` | ✅ Valid (biên dưới) |
| `EC_P_3` | Số nguyên âm | `-1`, `-100000` | ❌ Invalid |
| `EC_P_4` | Số thập phân (float) | `99.99`, `1500.5` | ❌ Invalid (DB lưu nhưng sai kiểu) |
| `EC_P_5` | Chuỗi không phải số | `"abc"`, `"giá rẻ"` | ❌ Invalid (DB lưu được do SQLite dynamic typing) |
| `EC_P_6` | Chuỗi trống `""` | `""` | ❌ Invalid |
| `EC_P_7` | Số nguyên cực lớn (> MAX_SAFE_INTEGER) | `9999999999999999` | ❌ Invalid (overflow JS/DB) |
| `EC_P_8` | Chuỗi số hợp lệ | `"100000"` | ⚠️ SQLite lưu được, nhưng gây lỗi logic |
| `EC_P_9` | `null` / `undefined` | `null` | ❌ Invalid |

### 1.4 Phân tích miền cho `category_id`

| Lớp tương đương | Mô tả | Hợp lệ? |
|---|---|---|
| `EC_C_1` | Integer tồn tại trong bảng categories (1, 2, 3) | ✅ Valid |
| `EC_C_2` | Integer không tồn tại (99, 9999) | ❌ Invalid (không có FK constraint trong SQLite) |
| `EC_C_3` | Chuỗi không phải số (`"abc"`) | ❌ Invalid |
| `EC_C_4` | Null / bỏ trống | ❌ Invalid |

---

## BƯỚC 2: Phân tích Giá trị biên (Boundary Value Analysis)

### 2.1 Biên của `price`

**Giới hạn dưới: 0 (giá trị nhỏ nhất hợp lệ)**

| Loại biên | Giá trị | Mô tả |
|---|---|---|
| Ngay tại biên (On) | `0` | Giá = 0, sản phẩm miễn phí — hợp lệ |
| Ngay dưới biên (Just below) | `-1` | Giá âm — không hợp lệ |
| Ngay trên biên (Just above) | `1` | Giá dương nhỏ nhất — hợp lệ |

**Giới hạn trên thực tế: Không được định nghĩa tường minh**  
Lấy `Number.MAX_SAFE_INTEGER = 9007199254740991` làm mốc tham chiếu JS:

| Loại biên | Giá trị | Mô tả |
|---|---|---|
| Ngay tại biên (On) | `9007199254740991` | MAX_SAFE_INTEGER — kết quả khó đoán |
| Ngay dưới biên (Just below) | `9007199254740990` | Trong phạm vi an toàn JS |
| Ngay trên biên (Just above) | `9007199254740992` | Vượt MAX_SAFE_INTEGER — mất độ chính xác |

**Biên nghiệp vụ tham chiếu từ seed data:**  
Sản phẩm cao nhất: `45,000,000 VNĐ` (MacBook Pro M3)

### 2.2 Biên của `name` (Trường required)

| Loại biên | Giá trị | Mô tả |
|---|---|---|
| Ngay tại biên dưới (On lower) | `"A"` (1 ký tự) | Tên ngắn nhất hợp lệ |
| Dưới biên (Below lower) | `""` (0 ký tự) | Rỗng — không hợp lệ |
| Biên khoảng trắng | `"   "` (3 dấu cách) | Không rỗng về mặt HTML nhưng vô nghĩa |

### 2.3 Biên kiểu dữ liệu `price` (Type Boundary)

| Loại biên | Giá trị | Kết quả mong đợi |
|---|---|---|
| Chuỗi số hợp lệ | `"50000"` | Backend nhận string, SQLite lưu dưới dạng TEXT — lỗi tiềm ẩn |
| Chuỗi không phải số | `"abc"` | SQLite lưu được, logic sai hoàn toàn |
| Float | `99.5` | SQLite lưu 99.5, khai báo INTEGER bị vi phạm |

---

## BƯỚC 3: Bảng Test Case Toàn diện

### Nhóm A — Giá trị `price` hợp lệ (Valid Domain)

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|---|---|---|---|---|
| FR15-A-01 | Giá tiền bình thường | `name="iPhone 15", price=30000000, category_id=1` | HTTP 200, `{"message":"Product created", "id": N}` — tạo thành công | Valid |
| FR15-A-02 | Giá = 0 (biên dưới — sản phẩm miễn phí) | `name="Free Gift", price=0, category_id=1` | HTTP 200, product được tạo với `price=0` | Valid |
| FR15-A-03 | Giá = 1 — ngay trên biên dưới | `name="SP giá 1đ", price=1, category_id=1` | HTTP 200, product được tạo với `price=1` | Valid |
| FR15-A-04 | Giá lớn hợp lệ (nghiệp vụ bình thường) | `name="MacBook Pro M4", price=45000000, category_id=2` | HTTP 200, sản phẩm được tạo với `price=45000000` | Valid |
| FR15-A-05 | Giá rất lớn nhưng trong MAX_SAFE_INTEGER | `name="SP siêu đắt", price=9007199254740990, category_id=1` | HTTP 200, DB lưu được — ghi nhận không có giới hạn trên | Valid |

### Nhóm B — Giá trị `price` âm (Invalid — Below Boundary)

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|---|---|---|---|---|
| FR15-B-01 | Giá = -1 — ngay dưới biên dưới | `name="SP lỗi", price=-1, category_id=1` | **FAIL thực tế:** HTTP 200, DB lưu `-1`. Mong đợi: HTTP 400 "Giá không được âm" | Invalid |
| FR15-B-02 | Giá âm lớn | `name="SP lỗi", price=-100000, category_id=1` | **FAIL thực tế:** HTTP 200, DB lưu `-100000`. Bug: Không có validation | Invalid |
| FR15-B-03 | Giá âm cực lớn | `name="SP lỗi", price=-9999999999, category_id=1` | **FAIL thực tế:** HTTP 200, DB lưu giá âm. Dữ liệu bẩn vào DB | Invalid |

### Nhóm C — Kiểu dữ liệu sai cho `price` (Type Mismatch — Critical)

| Test Case ID | Mô tả | Dữ liệu đầu vào (API trực tiếp) | Kết quả mong đợi | Loại |
|---|---|---|---|---|
| FR15-C-01 | `price` là chuỗi số — lỗ hổng từ frontend | `price: "50000"` (JSON string) | **FAIL:** HTTP 200, SQLite lưu `"50000"` TEXT. Bug: `price INTEGER` bị vi phạm | Invalid |
| FR15-C-02 | `price` là chuỗi chữ cái | `price: "abc"` | **FAIL:** HTTP 200, SQLite lưu `"abc"`. Critical Bug: Frontend hiển thị "abc ₫" | Invalid |
| FR15-C-03 | `price` là chuỗi hỗn hợp | `price: "100abc"` | **FAIL:** HTTP 200, SQLite lưu `"100abc"`. Bug: Không validation | Invalid |
| FR15-C-04 | `price` là chuỗi float | `price: "99.99"` | **FAIL:** HTTP 200, lưu dạng TEXT. Bug: Không phải INTEGER | Invalid |
| FR15-C-05 | `price` là số thực (float) | `price: 1500.5` | **FAIL:** HTTP 200, SQLite lưu `1500.5`. Bug: Schema khai báo INTEGER nhưng lưu REAL | Invalid |
| FR15-C-06 | `price` là chuỗi trống `""` | `price: ""` | **FAIL:** HTTP 200, DB lưu chuỗi rỗng. Bug: Giá trống không hợp lệ | Invalid |
| FR15-C-07 | `price` là `null` | `price: null` | **FAIL:** HTTP 200, DB lưu `NULL`. Bug: Giá null không hợp lệ | Invalid |
| FR15-C-08 | `price` bị bỏ qua (missing) | Body không có trường `price` | **FAIL:** HTTP 200, DB lưu `NULL`. Bug: Giá trống không có thông báo lỗi | Invalid |
| FR15-C-09 | `price` là boolean `true` | `price: true` | **FAIL:** HTTP 200, SQLite coerce `true` → `1`. Dữ liệu bị mất thông tin | Invalid |
| FR15-C-10 | `price` là array | `price: [100, 200]` | **FAIL:** HTTP 200 hoặc 500, DB gặp lỗi serialize. Bug: Không validate kiểu | Invalid |

### Nhóm D — Trường `name` rỗng / không hợp lệ (Required Field Violations)

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|---|---|---|---|---|
| FR15-D-01 | `name` rỗng qua UI | Submit form với ô name để trống | HTML5 `required` chặn tại browser — form không submit | Invalid |
| FR15-D-02 | `name` rỗng qua API (bypass UI) | `{name: "", price: 100, category_id: 1}` | **FAIL:** HTTP 200, sản phẩm tạo với `name=""`. Critical Bug: API thiếu server-side validation | Invalid |
| FR15-D-03 | `name` chỉ có dấu cách qua UI | Nhập `"   "` vào ô name rồi submit | **FAIL:** HTML5 `required` KHÔNG chặn được dấu cách. Form submit. Bug: Thiếu `trim()` validation | Invalid |
| FR15-D-04 | `name` là `null` qua API | `{name: null, price: 100, category_id: 1}` | **FAIL:** HTTP 200, sản phẩm tạo với `name=NULL`. Bug: Thiếu null check | Invalid |
| FR15-D-05 | `name` bị bỏ qua (missing) | `{price: 100, category_id: 1}` | **FAIL:** HTTP 200, sản phẩm tạo với `name=NULL`. Bug: API không validate required | Invalid |
| FR15-D-06 | `name` = 1 ký tự — biên dưới hợp lệ | `{name: "A", price: 100, category_id: 1}` | HTTP 200, sản phẩm được tạo với `name="A"` | Valid |
| FR15-D-07 | `name` = chuỗi rất dài (10,000 ký tự) | `name: "A".repeat(10000)` | HTTP 200 — SQLite TEXT không giới hạn, không bị lỗi | Valid* |

### Nhóm E — Giá trị `price` biên trên (Upper Boundary)

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|---|---|---|---|---|
| FR15-E-01 | Giá = MAX_SAFE_INTEGER JavaScript | `price: 9007199254740991` | **FAIL:** SQLite lưu nhưng giá trị có thể bị làm tròn do JS floating point. Bug: Không có giới hạn tối đa | Invalid |
| FR15-E-02 | Giá vượt MAX_SAFE_INTEGER | `price: 9007199254740992` | **FAIL:** JavaScript mất độ chính xác — giá bị sai. Bug: Không validation cận trên | Invalid |
| FR15-E-03 | Giá = 999,999,999 (~1 tỷ) — nghiệp vụ | `price: 999999999, name="SP siêu VIP"` | HTTP 200, sản phẩm được tạo. DB lưu được — ghi nhận | Valid |
| FR15-E-04 | Giá âm qua HTML input type=number | Nhập `-1` vào input Giá tiền trên UI | **FAIL:** `type="number"` không có `min=0` → Browser **cho phép** nhập số âm. Bug: Thiếu `min="0"` trên input | Invalid |

### Nhóm F — Trường `category_id` không hợp lệ

| Test Case ID | Mô tả | Dữ liệu đầu vào | Kết quả mong đợi | Loại |
|---|---|---|---|---|
| FR15-F-01 | `category_id` không tồn tại | `{name:"SP test", price:100, category_id: 9999}` | **FAIL:** HTTP 200, sản phẩm tạo với FK không tồn tại. Bug: SQLite không bật FOREIGN KEY enforcement | Invalid |
| FR15-F-02 | `category_id` = 0 | `{name:"SP test", price:100, category_id: 0}` | **FAIL:** HTTP 200. Bug: category_id 0 không hợp lệ | Invalid |
| FR15-F-03 | `category_id` là chuỗi | `{name:"SP test", price:100, category_id: "Electronics"}` | **FAIL:** HTTP 200, DB lưu chuỗi vào cột INTEGER. Bug: Không validate kiểu | Invalid |

---

## Tổng hợp Lỗi phát hiện được

| # | Mã lỗi | Mức độ | Vị trí | Mô tả |
|---|---|---|---|---|
| 1 | **BUG-15-01** | 🔴 CRITICAL | `server.js:167-177` | API `POST /api/products` không có bất kỳ validation nào — chấp nhận mọi kiểu dữ liệu cho `price` |
| 2 | **BUG-15-02** | 🔴 CRITICAL | `App.jsx:505-507` | `price` được lưu dưới dạng **string** trong state và gửi thẳng lên API — không có `parseFloat()` hay `parseInt()` |
| 3 | **BUG-15-03** | 🔴 CRITICAL | `server.js:167-177` | API không validate `name` là required — bypass UI dễ dàng tạo sản phẩm với `name=null` |
| 4 | **BUG-15-04** | 🟠 HIGH | `App.jsx:500-508` | Input `price` thiếu `min="0"` → người dùng có thể nhập giá âm qua UI |
| 5 | **BUG-15-05** | 🟠 HIGH | `App.jsx:491-498` | `name` chỉ có `required` HTML5 — khoảng trắng `"   "` vượt qua validation |
| 6 | **BUG-15-06** | 🟡 MEDIUM | `database.js` | SQLite không bật `PRAGMA foreign_keys = ON` → `category_id` không hợp lệ lưu không báo lỗi |
| 7 | **BUG-15-07** | 🟡 MEDIUM | `App.jsx:110-114` | Logic `PUT` sản phẩm: thay vì cập nhật 1 SP, code cập nhật `name` cho **TẤT CẢ** sản phẩm trong local state |
| 8 | **BUG-15-08** | 🟡 MEDIUM | `server.js:162` | `GET /api/products/:id` với id chẵn tự động chuyển price sang string: `row.price = row.price.toString()` — gây inconsistency |

---

## Ma trận phủ sóng Test (Coverage Matrix)

| Tiêu chí | Số TC | Phủ sóng |
|---|---|---|
| Giá trị hợp lệ (price ≥ 0) | 5 | Nhóm A |
| Giá trị âm (price < 0) | 3 | Nhóm B |
| Kiểu dữ liệu sai (type mismatch) | 10 | Nhóm C |
| Trường name rỗng/null | 7 | Nhóm D |
| Biên trên (upper boundary) | 4 | Nhóm E |
| category_id không hợp lệ | 3 | Nhóm F |
| **Tổng cộng** | **32** | **6 nhóm** |

---

## Khuyến nghị sửa lỗi

### Backend (`server.js`)

```js
app.post("/api/products", (req, res) => {
  const { name, price, description, imageUrl, category_id } = req.body;
  
  // 1. Validate name
  if (!name || typeof name !== 'string' || name.trim() === '') {
    return res.status(400).json({ error: "Tên sản phẩm không được để trống" });
  }
  
  // 2. Validate price
  const parsedPrice = Number(price);
  if (price === '' || price === null || price === undefined || isNaN(parsedPrice)) {
    return res.status(400).json({ error: "Giá phải là số hợp lệ" });
  }
  if (!Number.isInteger(parsedPrice) || parsedPrice < 0) {
    return res.status(400).json({ error: "Giá phải là số nguyên không âm" });
  }
  // ... tiếp tục với validated data
});
```

### Frontend (`App.jsx`)

```jsx
// 1. Thêm min="0" và required cho price input
input type="number" min="0" required placeholder="Giá tiền"

// 2. Ép kiểu price sang số và trim name khi submit
const payload = {
  ...productForm,
  price: parseInt(productForm.price, 10),  // ép kiểu trước khi gửi
  name: productForm.name.trim(),           // loại bỏ khoảng trắng đầu/cuối
};
```

---

*Báo cáo được tạo theo quy trình Domain Testing & BVA từ SKILL.MD*  
*Phiên bản: FR-15_TestReport.md v1.0*
