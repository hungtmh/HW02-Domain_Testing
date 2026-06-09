---
name: hw02-eshop-setup
description: >-
  Starts and configures the EShop SUT for HW02 testing on Windows. Use when the
  user cannot run EShop, mobile shows empty data, login fails on mobile, or
  needs backend/frontend/admin/mobile setup instructions.
---

# EShop Setup — HW02

## Khởi chạy (Windows PowerShell)

Cần **3–4 terminal riêng**, giữ chạy liên tục.

### Terminal 1 — Backend (bắt buộc)

```powershell
cd backend
npm install
node database.js    # lần đầu hoặc reset data
node server.js
```

Kiểm tra: http://localhost:3000/api/products trả JSON.

### Terminal 2 — Frontend Web

```powershell
cd frontend-web
npm install
npm run dev
```

→ http://localhost:5173

### Terminal 3 — Web Admin

```powershell
cd frontend-admin
npm install
npm run dev
```

→ http://localhost:5174

Nếu `Port 5174 is already in use`:

```powershell
netstat -ano | findstr :5174
taskkill /PID <PID> /F
```

### Terminal 4 — Mobile (Pool D)

```powershell
cd frontend-mobile
npm install
npx expo start
```

## Cấu hình Mobile API (quan trọng)

File: `frontend-mobile/App.js` dòng `API_URL`.

**Điện thoại thật (Expo Go)** — dùng IP LAN máy chạy backend:

```powershell
ipconfig
# Lấy IPv4, ví dụ 192.168.1.3
```

```javascript
const API_URL = "http://192.168.1.3:3000/api";
```

**Android Emulator**:

```javascript
const API_URL = "http://10.0.2.2:3000/api";
```

**KHÔNG** dùng `localhost` trên điện thoại — sẽ không kết nối được.

Sau đổi IP: reload Expo (`r` trong terminal).

## Tài khoản test

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@eshop.com | Admin123! |
| User | test@eshop.com | Test1234! |

## Coupon mẫu (FR-09)

| Mã | Ghi chú |
|----|---------|
| SAVE10 | 10%, min 300k |
| BIGBUY | 50k fixed, min 500k |
| EXPIRED | đã hết hạn |

## Troubleshooting

| Triệu chứng | Nguyên nhân | Cách sửa |
|-------------|-------------|----------|
| Mobile trống, login fail | Sai API_URL | Sửa IP theo ipconfig |
| Web không load sản phẩm | Backend chưa chạy | Start `node server.js` |
| Port đã dùng | Instance cũ | taskkill PID |
| Firewall chặn | Windows Firewall | Cho phép Node.js private network |

## Verify trước khi test

```powershell
Invoke-RestMethod http://localhost:3000/api/products
Invoke-RestMethod http://<LAN-IP>:3000/api/products
```

Cả hai phải trả danh sách sản phẩm.
