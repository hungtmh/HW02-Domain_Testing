&lt;!-- File: FR-20_TestReport.md --&gt;

# BÁO CÁO KIỂM THỬ: FR-20 — Mobile App: Giỏ Hàng & Thanh Toán (Cart & Checkout)

**Phiên bản:** 1.0  
**Ngày:** 2026-07-06  
**Người thực hiện:** Antigravity QA Agent (Claude Sonnet — Thinking Mode)  
**Phạm vi:** `frontend-mobile/App.js` — Logic nhập số lượng sản phẩm trong giỏ hàng (`renderCart`) và màn hình chi tiết sản phẩm (`renderProductDetail`), hàm `normalizeQuantity`, hàm `addToCart`, và công thức tính `cartTotal`.

---

## Tổng quan về SUT (System Under Test)

### Luồng nhập số lượng — 2 điểm nhập liệu

#### Điểm 1: Màn hình Chi Tiết Sản Phẩm (`renderProductDetail`, dòng 564–570)

```jsx
&lt;TextInput
  keyboardType="numeric"
  value={quantity}
  onChangeText={setQuantity}   // chỉ lưu chuỗi vào state, KHÔNG parse ngay
/&gt;
```

State `quantity` là chuỗi (`"1"` mặc định). Khi nhấn "Thêm vào giỏ", giá trị này được truyền vào `addToCart(product, quantity)`, rồi qua `normalizeQuantity`.

#### Điểm 2: Màn hình Giỏ Hàng (`renderCart`, dòng 611–623) ← **LỖ HỔNG CHÍNH**

```jsx
&lt;TextInput
  keyboardType="numeric"
  value={String(item.quantity ?? "")}
  onChangeText={(text) =&gt; {
    const newCart = [...cart];
    const parsed = parseInt(text, 10);          // (A) parse chuỗi nhập
    newCart[index].quantity =
      Number.isFinite(parsed) &amp;&amp; parsed &gt; 0
        ? parsed + 1                            // (B) BUG: cộng thừa 1!
        : 1;                                    // (C) fallback = 1
    setCart(newCart);
  }}
/&gt;
```

**Lỗi thiết kế nghiêm trọng tại dòng 620:** Khi `parsed` hợp lệ và > 0, giá trị được lưu là `parsed + 1` thay vì `parsed`. Điều này có nghĩa là mọi lần người dùng chỉnh sửa số lượng, giỏ hàng sẽ bị tăng thêm 1 đơn vị so với giá trị nhập.

#### Hàm `normalizeQuantity` (dòng 129–132)

```jsx
const normalizeQuantity = (value) =&gt; {
  const parsed = parseInt(value, 10);
  return Number.isFinite(parsed) &amp;&amp; parsed &gt; 0 ? parsed : 1;
};
```

Hàm này **ĐÚNG** — không có bug. Được dùng khi thêm sản phẩm vào giỏ (không dùng khi chỉnh sửa trong giỏ).

#### Công thức tính `cartTotal` (dòng 75–77)

```jsx
const cartTotal = useMemo(() =&gt; {
  return cart.reduce((total, item) =&gt; total + item.price * item.quantity, 0);
}, [cart]);
```

`cartTotal` nhân trực tiếp `item.price * item.quantity`. Vì `item.quantity` đã bị cộng thừa 1 từ bước nhập, tổng tiền sẽ **luôn sai**.

---

## Bước 1: Phân tích Miền Giá Trị (Domain Testing)

### Biến đầu vào cần phân tích

| Biến | Kiểu dữ liệu nhận vào | Nguồn xử lý | Mô tả |
|---|---|---|---|
| `text` (trong `onChangeText` của giỏ hàng) | `string` (từ React Native TextInput) | `parseInt(text, 10)` | Chuỗi người dùng gõ vào ô số lượng trong giỏ |
| `quantity` (trong `renderProductDetail`) | `string` (state) | `normalizeQuantity(quantity)` trong `addToCart` | Chuỗi người dùng gõ vào ô số lượng ở trang chi tiết |

### Phân tích miền giá trị cho `text` (input giỏ hàng)

#### Lớp tương đương VALID (sau khi `parseInt` cho kết quả hợp lệ và > 0)

| ID | Tên lớp | Mô tả | Ví dụ giá trị |
|---|---|---|---|
| EC-V1 | Số nguyên dương nhỏ | `parseInt(text)` trả về số nguyên trong [1, 99] | `"1"`, `"2"`, `"5"`, `"99"` |
| EC-V2 | Số nguyên dương lớn (< MAX_SAFE_INTEGER) | `parseInt(text)` trả về số nguyên trong [100, 999999] | `"100"`, `"999999"` |
| EC-V3 | Số thập phân có phần nguyên > 0 | `parseInt("1.9")` = 1 (hợp lệ, lấy phần nguyên) | `"1.9"`, `"5.7"`, `"2.0"` |
| EC-V4 | Chuỗi số kèm khoảng trắng đầu | `parseInt(" 3 ")` = 3 (JS bỏ whitespace đầu) | `" 3"`, `"  10  "` |
| EC-V5 | Chuỗi hỗn hợp bắt đầu bằng chữ số | `parseInt("3abc")` = 3 (JS lấy phần đầu) | `"3abc"`, `"2x5"` |

> **Lưu ý quan trọng:** Tất cả EC-V ở trên đều **kích hoạt bug** vì kết quả lưu = `parsed + 1`.

#### Lớp tương đương INVALID (sau khi `parseInt` trả về NaN hoặc <= 0 → fallback = 1)

| ID | Tên lớp | Mô tả | Ví dụ giá trị |
|---|---|---|---|
| EC-I1 | Số nguyên âm | `parseInt(text)` trả về số âm <= -1 | `"-1"`, `"-5"`, `"-999"` |
| EC-I2 | Số 0 | `parseInt("0")` = 0, không thỏa `> 0` | `"0"` |
| EC-I3 | Chuỗi rỗng | `parseInt("")` = NaN | `""` |
| EC-I4 | Chỉ chữ cái hoặc ký tự đặc biệt | `parseInt("abc")` = NaN | `"abc"`, `"!@#"`, `"hello"` |
| EC-I5 | Số thực âm | `parseInt("-1.5")` = -1 <= 0 | `"-1.5"`, `"-0.5"` |
| EC-I6 | Số 0 thập phân | `parseInt("0.9")` = 0 | `"0.9"`, `"0.1"` |
| EC-I7 | Chuỗi chỉ có khoảng trắng | `parseInt("   ")` = NaN | `"   "` |
| EC-I8 | Số cực lớn (> Number.MAX_SAFE_INTEGER) | `parseInt` vẫn trả số nhưng mất độ chính xác | `"9007199254740992"` |
| EC-I9 | Chuỗi hex prefix | `parseInt("0xFF")` = 255 (hợp lệ nhưng ngoài ý muốn) | `"0xFF"` |

---

## Bước 2: Phân tích Giá Trị Biên (BVA)

### BVA cho điều kiện `parsed > 0` (ranh giới hợp lệ/không hợp lệ)

| Loại biên | Giá trị `parsed` | Input ví dụ | Kết quả theo code | Kết quả đúng phải là | Sai? |
|---|---|---|---|---|---|
| Just below (invalid side) | -1 | `"-1"` | 1 (fallback) | 1 (fallback) | Không (nhưng không cảnh báo) |
| On the boundary (invalid) | 0 | `"0"` | 1 (fallback) | 1 (fallback) | Không |
| Just above (valid — MIN) | 1 | `"1"` | **2** (parsed+1) | **1** | **CÓ — BUG** |
| Nominal valid | 2 | `"2"` | **3** (parsed+1) | **2** | **CÓ — BUG** |
| Biên trên thực tế | 99 | `"99"` | **100** (parsed+1) | **99** | **CÓ — BUG** |
| Số lớn | 1000000 | `"1000000"` | **1000001** | **1000000** | **CÓ — BUG** |

### BVA cho `parseInt(text, 10)` — ranh giới NaN vs. số hợp lệ

| Loại biên | Input | `parseInt` trả | Kết quả `quantity` | Ghi chú |
|---|---|---|---|---|
| NaN side — chỉ chữ cái | `"abc"` | NaN | 1 (fallback) | Đúng hành vi |
| NaN → số — chuỗi hỗn hợp bắt đầu số | `"1abc"` | 1 | **2** (1+1) | BUG: lẽ ra nên từ chối |
| Thập phân — phần nguyên = 0 | `"0.9"` | 0 | 1 (fallback) | Fallback, không phản ánh ý định |
| Thập phân — phần nguyên = 1 | `"1.9"` | 1 | **2** (1+1) | BUG: lẽ ra = 1 |
| Thập phân — phần nguyên lớn | `"5.99"` | 5 | **6** (5+1) | BUG |
| Âm sát biên | `"-1"` | -1 | 1 (fallback) | Hành vi đúng nhưng không cảnh báo |
| Cực lớn (overflow) | `"9999999999999999"` | 10000000000000000 | 10000000000000001 | Lỗi số học float |
| Hex | `"0xFF"` | 255 | **256** | BUG ẩn: người dùng nhập hex |

---

## Bước 3: Bảng Test Case Toàn Diện

### Nhóm A — Số nguyên dương (EC-V1, EC-V2) — Kịch bản kiểm tra bug chính

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (Inputs) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (theo code) | Loại (Valid/Invalid) | Mức độ |
|---|---|---|---|---|---|---|
| FR20-TC-A01 | Nhập số lượng tối thiểu hợp lệ = 1 | `text = "1"` | quantity = 1; cartTotal = price × 1 | quantity = **2**; cartTotal = price × **2** | Invalid (Bug) | CRITICAL |
| FR20-TC-A02 | Nhập số lượng = 2 | `text = "2"` | quantity = 2; cartTotal = price × 2 | quantity = **3**; cartTotal = price × **3** | Invalid (Bug) | CRITICAL |
| FR20-TC-A03 | Nhập số lượng bình thường = 5 | `text = "5"` | quantity = 5; cartTotal = price × 5 | quantity = **6**; cartTotal = price × **6** | Invalid (Bug) | CRITICAL |
| FR20-TC-A04 | Nhập số lượng = 10 | `text = "10"` | quantity = 10; cartTotal = price × 10 | quantity = **11**; cartTotal = price × **11** | Invalid (Bug) | CRITICAL |
| FR20-TC-A05 | Nhập số lượng biên trên thực tế = 99 | `text = "99"` | quantity = 99; cartTotal = price × 99 | quantity = **100**; cartTotal = price × **100** | Invalid (Bug) | CRITICAL |
| FR20-TC-A06 | Nhập số lượng = 100 | `text = "100"` | quantity = 100; cartTotal = price × 100 | quantity = **101** | Invalid (Bug) | CRITICAL |

### Nhóm B — Số không hợp lệ: âm, zero (EC-I1, EC-I2) — Kiểm tra fallback

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (Inputs) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (theo code) | Loại (Valid/Invalid) | Mức độ |
|---|---|---|---|---|---|---|
| FR20-TC-B01 | Nhập 0 (ranh giới không hợp lệ) | `text = "0"` | quantity = 1 (fallback); hiện cảnh báo | quantity = 1; **không cảnh báo** | Invalid (hành vi khớp, thiếu UX) | MEDIUM |
| FR20-TC-B02 | Nhập -1 (just below biên) | `text = "-1"` | quantity = 1 (fallback); hiện cảnh báo | quantity = 1; **không cảnh báo** | Invalid (hành vi khớp, thiếu UX) | MEDIUM |
| FR20-TC-B03 | Nhập số âm lớn = -999 | `text = "-999"` | quantity = 1 (fallback) | quantity = 1 | Invalid (hành vi khớp) | LOW |
| FR20-TC-B04 | Nhập số âm nhỏ = -1000000 | `text = "-1000000"` | quantity = 1 (fallback) | quantity = 1 | Invalid (hành vi khớp) | LOW |

### Nhóm C — Chuỗi không phải số (EC-I3, EC-I4, EC-I7) — Kiểm tra NaN handling

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (Inputs) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (theo code) | Loại (Valid/Invalid) | Mức độ |
|---|---|---|---|---|---|---|
| FR20-TC-C01 | Nhập chuỗi chữ cái thuần | `text = "abc"` | quantity = 1 (fallback) | quantity = 1 | Invalid (hành vi khớp) | LOW |
| FR20-TC-C02 | Nhập chuỗi rỗng (xóa hết nội dung) | `text = ""` | quantity giữ nguyên giá trị cũ | quantity = **1** (fallback tức thì) | Invalid (hành vi khác kỳ vọng) | MEDIUM |
| FR20-TC-C03 | Nhập ký tự đặc biệt | `text = "!@#$"` | quantity = 1 (fallback) | quantity = 1 | Invalid (hành vi khớp) | LOW |
| FR20-TC-C04 | Nhập khoảng trắng | `text = "   "` | quantity = 1 (fallback) | quantity = 1 | Invalid (hành vi khớp) | LOW |
| FR20-TC-C05 | Nhập ký tự Unicode / tiếng Việt | `text = "hai"` | quantity = 1 (fallback) | quantity = 1 | Invalid (hành vi khớp) | LOW |
| FR20-TC-C06 | Nhập emoji | `text = "😀"` | quantity = 1 (fallback) | quantity = 1 | Invalid (hành vi khớp) | LOW |

### Nhóm D — Chuỗi hỗn hợp (EC-V5) — parseInt lấy phần đầu

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (Inputs) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (theo code) | Loại (Valid/Invalid) | Mức độ |
|---|---|---|---|---|---|---|
| FR20-TC-D01 | Chuỗi bắt đầu bằng "1", theo sau là chữ | `text = "1abc"` | Từ chối (không phải số nguyên thuần) | quantity = **2** (parseInt=1, +1) | Invalid (Bug) | HIGH |
| FR20-TC-D02 | Chuỗi bắt đầu bằng "3", theo sau là ký tự | `text = "3x5"` | Từ chối hoặc quantity = 3 | quantity = **4** (parseInt=3, +1) | Invalid (Bug) | HIGH |
| FR20-TC-D03 | Chuỗi bắt đầu bằng số, kèm khoảng trắng sau | `text = "5 kg"` | Từ chối hoặc quantity = 5 | quantity = **6** (parseInt=5, +1) | Invalid (Bug) | HIGH |
| FR20-TC-D04 | Chuỗi chữ trước số | `text = "abc3"` | quantity = 1 (fallback do NaN) | quantity = 1 | Invalid (hành vi khớp) | LOW |

### Nhóm E — Số thập phân (EC-V3, EC-I5, EC-I6) — parseInt cắt bỏ phần thập phân

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (Inputs) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (theo code) | Loại (Valid/Invalid) | Mức độ |
|---|---|---|---|---|---|---|
| FR20-TC-E01 | Nhập thập phân có phần nguyên = 1 | `text = "1.9"` | Từ chối hoặc quantity = 1 | quantity = **2** (parseInt=1, +1) | Invalid (Bug) | HIGH |
| FR20-TC-E02 | Nhập thập phân có phần nguyên = 5 | `text = "5.7"` | Từ chối hoặc quantity = 5 | quantity = **6** (parseInt=5, +1) | Invalid (Bug) | HIGH |
| FR20-TC-E03 | Nhập thập phân 0 < x < 1 (phần nguyên = 0) | `text = "0.9"` | quantity = 1 (fallback) | quantity = 1 (parseInt=0, fallback) | Invalid (hành vi khớp) | MEDIUM |
| FR20-TC-E04 | Nhập thập phân âm gần 0 | `text = "-0.5"` | quantity = 1 (fallback) | quantity = 1 (parseInt=0, fallback) | Invalid (hành vi khớp) | LOW |
| FR20-TC-E05 | Nhập thập phân âm | `text = "-1.5"` | quantity = 1 (fallback) | quantity = 1 (parseInt=-1, fallback) | Invalid (hành vi khớp) | LOW |
| FR20-TC-E06 | Nhập "2.0" (thực chất là 2) | `text = "2.0"` | quantity = 2 | quantity = **3** (parseInt=2, +1) | Invalid (Bug) | HIGH |

### Nhóm F — Số cực lớn và trường hợp đặc biệt (EC-I8, EC-I9)

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (Inputs) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (theo code) | Loại (Valid/Invalid) | Mức độ |
|---|---|---|---|---|---|---|
| FR20-TC-F01 | Số cực lớn vượt MAX_SAFE_INTEGER | `text = "9007199254740992"` | Từ chối hoặc giới hạn tối đa | quantity = 9007199254740993 (precision error) | Invalid (Bug tiềm ẩn) | HIGH |
| FR20-TC-F02 | Chuỗi hex hợp lệ | `text = "0xFF"` | Từ chối (= 255 ngoài ý muốn) | quantity = **256** (parseInt=255, +1) | Invalid (Bug ẩn) | MEDIUM |
| FR20-TC-F03 | Số rất lớn nhưng hợp lệ = 999999 | `text = "999999"` | quantity = 999999; cartTotal đúng | quantity = **1000000**; cartTotal sai | Invalid (Bug) | CRITICAL |
| FR20-TC-F04 | Chỉ dấu trừ | `text = "-"` | quantity = 1 (fallback) | quantity = 1 (parseInt=NaN) | Invalid (hành vi khớp) | LOW |
| FR20-TC-F05 | Dấu cộng trước số | `text = "+5"` | quantity = 5 hoặc từ chối | quantity = **6** (parseInt("+5")=5, +1) | Invalid (Bug) | HIGH |

### Nhóm G — Kiểm thử hàm `normalizeQuantity` (dùng khi thêm từ trang chi tiết — KHÔNG bị bug)

| Test Case ID | Mô tả (Description) | Dữ liệu đầu vào (Inputs) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (theo code) | Loại (Valid/Invalid) |
|---|---|---|---|---|---|
| FR20-TC-G01 | Thêm sp với quantity = "1" từ trang chi tiết | `quantity = "1"` qua normalizeQuantity | quantity thêm vào = 1 | quantity = 1 (PASS) | Valid |
| FR20-TC-G02 | Thêm sp với quantity = "5" | `quantity = "5"` qua normalizeQuantity | quantity = 5 | quantity = 5 (PASS) | Valid |
| FR20-TC-G03 | Thêm sp với quantity = "0" | `quantity = "0"` qua normalizeQuantity | quantity = 1 (fallback) | quantity = 1 (PASS) | Invalid (hành vi đúng) |
| FR20-TC-G04 | Thêm sp với quantity = "abc" | `quantity = "abc"` qua normalizeQuantity | quantity = 1 (fallback) | quantity = 1 (PASS) | Invalid (hành vi đúng) |
| FR20-TC-G05 | Thêm sp với quantity = "-5" | `quantity = "-5"` qua normalizeQuantity | quantity = 1 (fallback) | quantity = 1 (PASS) | Invalid (hành vi đúng) |

---

## Tổng hợp Bug Phát Hiện

| Bug ID | Vị trí | Mức độ | Mô tả | Ảnh hưởng |
|---|---|---|---|---|
| BUG-FR20-01 | `App.js` dòng 620 | CRITICAL | `parsed + 1` thay vì `parsed` khi lưu số lượng vào giỏ hàng | Mọi lần chỉnh sửa số lượng sẽ tăng thừa 1, gây sai `cartTotal` và sai tổng thanh toán |
| BUG-FR20-02 | `App.js` dòng 617–621 | HIGH | Không validate chuỗi hỗn hợp (ví dụ `"3abc"`) — `parseInt` vẫn trích xuất số 3 | Người dùng nhập sai format vẫn được chấp nhận, sau đó bị +1 thêm |
| BUG-FR20-03 | `App.js` dòng 617–621 | HIGH | Số thập phân (`"1.9"`) bị cắt thành 1 rồi cộng thêm 1 thành 2 | Người dùng nhập `"1.9"` nhận được quantity = 2, không khớp ý định |
| BUG-FR20-04 | `App.js` dòng 617–621 | MEDIUM | Khi xóa hết nội dung ô nhập, quantity tức thì reset về 1 | Trải nghiệm người dùng kém, không thể gõ số 2 chữ số mà không bị reset giữa chừng |
| BUG-FR20-05 | `App.js` dòng 391 | CRITICAL | `cart.slice(0, -1)` cắt bỏ sản phẩm cuối khi checkout nếu có > 1 sản phẩm | Đơn hàng gửi lên backend thiếu mặt hàng cuối cùng trong giỏ |
| BUG-FR20-06 | `App.js` dòng 617 | MEDIUM | Không giới hạn số lượng tối đa — có thể nhập `999999999` | Có thể gây overflow hoặc lỗi tài chính khi tính tổng tiền |

---

## Đề xuất sửa lỗi (BUG-FR20-01)

**Code hiện tại (SAI):**
```jsx
newCart[index].quantity =
  Number.isFinite(parsed) && parsed > 0
    ? parsed + 1   // BUG
    : 1;
```

**Code đề xuất (ĐÚNG):**
```jsx
newCart[index].quantity =
  Number.isFinite(parsed) && parsed > 0
    ? parsed        // FIX: lưu đúng giá trị đã parse
    : 1;
```

Ngoài ra nên thêm giới hạn tối đa và cảnh báo UX khi nhập sai:
```jsx
const MAX_QUANTITY = 999;
const clipped = Math.min(parsed, MAX_QUANTITY);
newCart[index].quantity =
  Number.isFinite(clipped) && clipped > 0 ? clipped : 1;
if (!Number.isFinite(parsed) || parsed <= 0) {
  Alert.alert("Số lượng không hợp lệ", "Vui lòng nhập số nguyên dương.");
}
```

---

## Tóm tắt kết quả kiểm thử

| Nhóm | Số TC | PASS | FAIL |
|---|---|---|---|
| A — Số nguyên dương | 6 | 0 | **6** |
| B — Số âm / zero | 4 | 4 | 0 |
| C — Chuỗi không phải số | 6 | 5 | 1 |
| D — Chuỗi hỗn hợp | 4 | 1 | **3** |
| E — Số thập phân | 6 | 3 | **3** |
| F — Số cực lớn / đặc biệt | 5 | 1 | **4** |
| G — normalizeQuantity | 5 | 5 | 0 |
| **TỔNG** | **36** | **19** | **17** |

> **Tỷ lệ lỗi: 47%** — Đặc biệt nghiêm trọng vì **100% kịch bản nhập số hợp lệ đều cho kết quả sai** do bug `parsed + 1`.
