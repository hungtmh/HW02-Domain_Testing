# Consolidated Bug Report - EShop Testing

**Họ và tên:** Nguyễn Tấn Thắng  
**Nhóm:** Nhóm 08  
**MSSV:** 23127259  
**Ngày cập nhật:** 2026-07-06  
**SUT:** Web Client + Web Admin + Mobile App + API Backend

**Evidence run:** 2026-07-05 20:13 ICT, test data prefix `live_hw02_1783257224503`. Ảnh/video bug trong các thư mục evidence là minh chứng từ thao tác UI/API trực tiếp trên EShop SUT. Riêng FR-07 BUG-003 dùng video `.mov`; PDF dùng ảnh preview để hiển thị ổn định.

---

# Bug Report - FR-02 Login and Account Lockout

## BUG-FR02-001: Failed login counter increases by 2 instead of 1

- **GitHub Issue:** [#27](https://github.com/hungtmh/HW02-Domain_Testing/issues/27)

- **Severity:** Major
- **Priority:** High
- **Component:** API Backend
- **Related test cases:** FR02-TC04, FR02-TC05, FR02-TC06

**Expected:** After one wrong password, `login_attempts = 1`; after two wrong passwords, `login_attempts = 2` and the account is not locked yet.

**Actual:** After one wrong password, `login_attempts = 2`; after two wrong passwords, `login_attempts = 4` and `locked_until` is created.

**Evidence:**

![BUG-FR02-001](./FR-02_bugs/BUG-001.png)

---

## BUG-FR02-002: Account lockout duration is 180 seconds instead of 30 seconds

- **GitHub Issue:** [#28](https://github.com/hungtmh/HW02-Domain_Testing/issues/28)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** API Backend
- **Related test cases:** FR02-TC07

**Expected:** Account is locked for about 30 seconds.

**Actual:** Account is locked for about 180 seconds because backend uses `Date.now() + 180000`.

**Evidence:**

![BUG-FR02-002](./FR-02_bugs/BUG-002.png)

---

## BUG-FR02-003: Login email field does not use `type="email"`

- **GitHub Issue:** [#29](https://github.com/hungtmh/HW02-Domain_Testing/issues/29)

- **Severity:** Minor
- **Priority:** Medium
- **Component:** Frontend Web Login
- **Related test cases:** FR02-TC03

**Expected:** Login email field uses HTML5 `type="email"`.

**Actual:** Login form uses label `Username` and input `type="text"`.

**Evidence:**

![BUG-FR02-003](./FR-02_bugs/BUG-003.png)

---

# Bug Report - FR-07 Shopping Cart

## BUG-FR07-001: Adding same product creates duplicate rows

- **GitHub Issue:** [#30](https://github.com/hungtmh/HW02-Domain_Testing/issues/30)

- **Severity:** Major
- **Priority:** High
- **Component:** Cart API / Frontend Cart Context
- **Related test cases:** FR07-TC03

**Expected:** Adding the same product twice produces one row with `quantity = 2`.

**Actual:** Cart creates duplicate rows for the same product.

**Evidence:**

![BUG-FR07-001](./FR-07_bugs/BUG-001.png)

---

## BUG-FR07-002: Cart quantity has no `+/-` controls

- **GitHub Issue:** [#31](https://github.com/hungtmh/HW02-Domain_Testing/issues/31)

- **Severity:** Major
- **Priority:** High
- **Component:** Frontend Web Cart
- **Related test cases:** FR07-TC04

**Expected:** Quantity column has `+` and `-` controls.

**Actual:** Quantity is shown as plain text.

**Evidence:**

![BUG-FR07-002](./FR-07_bugs/BUG-002.png)

---

## BUG-FR07-003: Delete cart item does not show confirmation dialog

- **GitHub Issue:** [#32](https://github.com/hungtmh/HW02-Domain_Testing/issues/32)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Frontend Web Cart
- **Related test cases:** FR07-TC05

**Expected:** Clicking `Xóa` shows a confirmation dialog before removing the item.

**Actual:** The item is removed immediately without a confirm dialog.

**Video Evidence:**

<video controls src="./FR-07_bugs/BUG-003.mov" width="720"></video>

[Open video evidence: BUG-003.mov](./FR-07_bugs/BUG-003.mov)

**PDF Preview:**

![BUG-FR07-003 preview](./FR-07_bugs/BUG-003-preview.png)

---

## BUG-FR07-004: Cart total label is wrong

- **GitHub Issue:** [#33](https://github.com/hungtmh/HW02-Domain_Testing/issues/33)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Frontend Web Cart
- **Related test cases:** FR07-TC07

**Expected:** Total label is `Tổng cộng`.

**Actual:** UI shows `Tổng tạm tính`.

**Evidence:**

![BUG-FR07-004](./FR-07_bugs/BUG-004.png)

---

## BUG-FR07-005: Empty cart has no illustration

- **GitHub Issue:** [#34](https://github.com/hungtmh/HW02-Domain_Testing/issues/34)

- **Severity:** Minor
- **Priority:** Low
- **Component:** Frontend Web Cart
- **Related test cases:** FR07-TC01

**Expected:** Empty cart has an illustration/icon and a clear message.

**Actual:** Empty cart only shows text and a continue shopping link.

**Evidence:**

![BUG-FR07-005](./FR-07_bugs/BUG-005.png)

---

# Bug Report - FR-16 Product Import from CSV

## BUG-FR16-001: Normal user can call admin product import API

- **GitHub Issue:** [#35](https://github.com/hungtmh/HW02-Domain_Testing/issues/35)

- **Severity:** Critical
- **Priority:** High
- **Component:** API Backend / Access Control
- **Related test cases:** FR16-TC04

**Expected:** Normal user token is rejected with HTTP 403 and no product is inserted.

**Actual:** Normal user token receives HTTP 200 and the product is inserted.

**Evidence:**

![BUG-FR16-001](./FR-16_bugs/BUG-001.png)

---

## BUG-FR16-002: Product import is not atomic when a row is invalid

- **GitHub Issue:** [#36](https://github.com/hungtmh/HW02-Domain_Testing/issues/36)

- **Severity:** Major
- **Priority:** High
- **Component:** API Backend / Database
- **Related test cases:** FR16-TC05

**Expected:** If any row is invalid, the whole import is rejected and rolled back.

**Actual:** API reports `inserted = 1/2`; the valid row is still inserted even though another row has an error.

**Evidence:**

![BUG-FR16-002 step 1](./FR-16_bugs/BUG-002-1.png)

![BUG-FR16-002 step 2](./FR-16_bugs/BUG-002-2.png)

---

## BUG-FR16-003: Product import accepts negative price

- **GitHub Issue:** [#37](https://github.com/hungtmh/HW02-Domain_Testing/issues/37)

- **Severity:** Major
- **Priority:** High
- **Component:** API Backend Validation
- **Related test cases:** FR16-TC06

**Expected:** Product with `price <= 0` is rejected.

**Actual:** Product with negative price is inserted.

**Evidence:**

![BUG-FR16-003](./FR-16_bugs/BUG-003.png)

---

## BUG-FR16-004: CSV parser does not support quoted commas

- **GitHub Issue:** [#38](https://github.com/hungtmh/HW02-Domain_Testing/issues/38)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Web Admin CSV Import
- **Related test cases:** FR16-TC07

**Expected:** CSV fields wrapped in double quotes can contain commas.

**Actual:** Admin parser uses `line.split(",")`, so quoted commas break the column mapping.

**Evidence:**

![BUG-FR16-004](./FR-16_bugs/BUG-004.png)

---

# Bug Report - Mobile Product Listing/Search

## BUG-MOB-001: Mobile API URL is hard-coded

- **GitHub Issue:** [#39](https://github.com/hungtmh/HW02-Domain_Testing/issues/39)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Mobile App Config
- **Related test cases:** MOB-TC05

**Expected:** API URL is configurable by environment/device.

**Actual:** `API_URL` is hard-coded to a LAN IP, making product listing/search fail on other devices or emulators.

**Evidence:**

![BUG-MOB-001](./Mobile-product-listing_bugs/BUG-001.jpg)

---

## BUG-MOB-002: Search query is not URL-encoded

- **GitHub Issue:** [#40](https://github.com/hungtmh/HW02-Domain_Testing/issues/40)

- **Severity:** Major
- **Priority:** High
- **Component:** Mobile Product Search
- **Related test cases:** MOB-TC04

**Expected:** Search keyword with special characters is URL-encoded.

**Actual:** Search query is concatenated directly into the URL.

**Evidence:**

![BUG-MOB-002](./Mobile-product-listing_bugs/BUG-002.jpg)

---

## BUG-MOB-003: Product search has no empty state

- **GitHub Issue:** [#41](https://github.com/hungtmh/HW02-Domain_Testing/issues/41)

- **Severity:** Medium
- **Priority:** Medium
- **Component:** Mobile Product Listing
- **Related test cases:** MOB-TC03

**Expected:** No-result search shows a clear empty state message.

**Actual:** Empty result does not show a proper empty state.

**Evidence:**

![BUG-MOB-003](./Mobile-product-listing_bugs/BUG-003.jpg)

---

## BUG-MOB-004: Product images use `resizeMode="stretch"`

- **GitHub Issue:** [#42](https://github.com/hungtmh/HW02-Domain_Testing/issues/42)

- **Severity:** Minor
- **Priority:** Low
- **Component:** Mobile Product Listing / Detail
- **Related test cases:** MOB-TC07

**Expected:** Product images preserve their aspect ratio.

**Actual:** Product images are stretched and can appear distorted.

**Evidence:**

![BUG-MOB-004](./Mobile-product-listing_bugs/BUG-004.jpg)

---

## GitHub Issues

Các bug đã được tạo issue thật trên GitHub repo nhóm để team có thể theo dõi và xử lý:

- **BUG-FR02-001:** [#27](https://github.com/hungtmh/HW02-Domain_Testing/issues/27) - [23127259][BUG-FR02-001] Failed login counter increases by 2 instead of 1
- **BUG-FR02-002:** [#28](https://github.com/hungtmh/HW02-Domain_Testing/issues/28) - [23127259][BUG-FR02-002] Account lockout duration is 180 seconds instead of 30 seconds
- **BUG-FR02-003:** [#29](https://github.com/hungtmh/HW02-Domain_Testing/issues/29) - [23127259][BUG-FR02-003] Login email field does not use type="email"
- **BUG-FR07-001:** [#30](https://github.com/hungtmh/HW02-Domain_Testing/issues/30) - [23127259][BUG-FR07-001] Adding same product creates duplicate rows
- **BUG-FR07-002:** [#31](https://github.com/hungtmh/HW02-Domain_Testing/issues/31) - [23127259][BUG-FR07-002] Cart quantity has no +/- controls
- **BUG-FR07-003:** [#32](https://github.com/hungtmh/HW02-Domain_Testing/issues/32) - [23127259][BUG-FR07-003] Delete cart item does not show confirmation dialog
- **BUG-FR07-004:** [#33](https://github.com/hungtmh/HW02-Domain_Testing/issues/33) - [23127259][BUG-FR07-004] Cart total label is wrong
- **BUG-FR07-005:** [#34](https://github.com/hungtmh/HW02-Domain_Testing/issues/34) - [23127259][BUG-FR07-005] Empty cart has no illustration
- **BUG-FR16-001:** [#35](https://github.com/hungtmh/HW02-Domain_Testing/issues/35) - [23127259][BUG-FR16-001] Normal user can call admin product import API
- **BUG-FR16-002:** [#36](https://github.com/hungtmh/HW02-Domain_Testing/issues/36) - [23127259][BUG-FR16-002] Product import is not atomic when a row is invalid
- **BUG-FR16-003:** [#37](https://github.com/hungtmh/HW02-Domain_Testing/issues/37) - [23127259][BUG-FR16-003] Product import accepts negative price
- **BUG-FR16-004:** [#38](https://github.com/hungtmh/HW02-Domain_Testing/issues/38) - [23127259][BUG-FR16-004] CSV parser does not support quoted commas
- **BUG-MOB-001:** [#39](https://github.com/hungtmh/HW02-Domain_Testing/issues/39) - [23127259][BUG-MOB-001] Mobile API URL is hard-coded
- **BUG-MOB-002:** [#40](https://github.com/hungtmh/HW02-Domain_Testing/issues/40) - [23127259][BUG-MOB-002] Search query is not URL-encoded
- **BUG-MOB-003:** [#41](https://github.com/hungtmh/HW02-Domain_Testing/issues/41) - [23127259][BUG-MOB-003] Product search has no empty state
- **BUG-MOB-004:** [#42](https://github.com/hungtmh/HW02-Domain_Testing/issues/42) - [23127259][BUG-MOB-004] Product images use resizeMode="stretch"

Evidence chính thức vẫn nằm trong các thư mục `reports/*_bugs/` và được link trong từng issue.
