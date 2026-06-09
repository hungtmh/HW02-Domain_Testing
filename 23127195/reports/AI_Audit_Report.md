# AI Audit Report — MSSV 23127195 — HW02

**Khai báo:** Tôi sử dụng AI tools cho các tác vụ sau trong bài HW02 Domain Testing.

**Công cụ sử dụng:** Cursor (Claude)

---

## Interaction 001

| Field | Nội dung |
|-------|----------|
| Tool | Cursor |
| Date & Time | 2026-06-08 ~15:30 |
| Feature | FR-01 Account Registration |
| Task | Chạy full hw02-workflow — Domain Testing + BVA + test execution |

### Prompt (nguyên văn)

```
@.cursor/skills/hw02-workflow/SKILL.md FR-01 Account-registration
```

### AI Output (tóm tắt)

- Đọc SRS FR-01, `Register.jsx`, `server.js`, `database.js`
- Tạo báo cáo Domain Testing (13 TC), BVA (16 TC)
- Chạy 8 API tests — phát hiện backend không validate
- Ghi bug reports BUG-001, BUG-006 và gap analysis

### Human Review

- Cần bổ sung: chạy UI tests trên browser, screenshot, GitHub Issues
- Cần bổ sung: BUG-002 đến BUG-005, BUG-007, BUG-008 file riêng
- Đánh giá: **Đúng hướng** — sinh viên cần verify và chụp ảnh trước khi nộp

---

## Interaction 002

| Field | Nội dung |
|-------|----------|
| Tool | Antigravity AI Coding Assistant |
| Date & Time | 2026-06-09 ~11:32 |
| Feature | FR-01 Account Registration |
| Task | Làm lại quy trình kiểm thử (Domain Testing + BVA + Bug Reports + Gap Analysis) |

### Prompt (nguyên văn)

```
Bạn hãy làm lại skill hw02-workflow cho FR-01: Đăng ký tài khoản 

Con cursor nó làm hơi không đúng ý 
```

### AI Output (tóm tắt)

- Phân tích mã nguồn SUT (`Register.jsx` frontend, `server.js` backend, `database.js` database schema).
- Thiết kế lại báo cáo Domain Testing ([FR-01_domain-testing.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_domain-testing.md)) gồm 13 test cases chuẩn đặc tả SRS.
- Thiết kế lại báo cáo BVA ([FR-01_bva.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bva.md)) gồm 12 test cases và kịch bản Robustness.
- Khởi động server backend và thực hiện các cuộc gọi API kiểm thử bằng PowerShell `Invoke-RestMethod` để kiểm định tính năng.
- Viết lại báo cáo thực thi ([FR-01_test-execution.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_test-execution.md)) ghi nhận 11 trường hợp thất bại (Fail) do hệ thống bỏ trống xác thực.
- Tạo chi tiết các báo cáo lỗi từ `BUG-001` đến `BUG-009` trong thư mục [FR-01_bugs](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bugs) (lỗi trùng email, mật khẩu plaintext, regex sai, thiếu confirmPassword, v.v.).
- Lập báo cáo Gap Analysis ([FR-01_ai-gap-analysis.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_ai-gap-analysis.md)) phân tích các điểm yếu của AI khi không đọc sâu mã nguồn.

### Human Review
- Đã sửa: Rà soát lại toàn bộ test cases, chỉnh sửa phân vùng và kiểm chứng phản hồi thực tế của server để đảm bảo kết quả chính xác 100%.
- Đánh giá: Rất đầy đủ và chi tiết hơn nhiều so với Cursor phiên bản trước, đã bao phủ được cả tầng bảo mật và kiểm thử bypass API.

---

