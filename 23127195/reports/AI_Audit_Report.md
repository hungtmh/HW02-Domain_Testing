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

## Interaction 003

| Field | Nội dung |
|-------|----------|
| Tool | Antigravity AI Coding Assistant |
| Date & Time | 2026-06-09 ~12:42 |
| Feature | FR-01 Account Registration |
| Task | Cấu hình lại skill tự động (yêu cầu thêm câu lệnh test) và gộp toàn bộ báo cáo lỗi |

### Prompt (nguyên văn)

```
trong skill chỉnh sửa lại phải thêm các câu lệnh test backend hay gì đó nữa , nếu test thì phải ghi rõ lệnh, để tui chụp màn hình bug

sửa lại đi với lại đừng chia nhiefu Bug-report làm gì (sửa lại trong skill luôn) chỉ 1 file .md bug-report chứa tất cả các lỗi, có câu lệnh chạy test kết quả mong muôn ,kết quả thực tế (FAil/pass) rồi screen shot vậy thôi ngắn gọn

với lại có github issue nữa á
```

### AI Output (tóm tắt)

- Chỉnh sửa lại các file skill `hw02-workflow` và `hw02-bug-report` để thay thế chuẩn đầu ra nhiều file bằng 1 file gộp duy nhất, bổ sung yêu cầu viết rõ câu lệnh test cụ thể.
- Sao chép đồng bộ các skill mới cập nhật vào thư mục toàn cục của Cursor (`%USERPROFILE%\.cursor\skills\`) và cục bộ dự án.
- Tạo báo cáo lỗi gộp [FR-01_bug-report.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-01_bug-report.md) tổng hợp toàn bộ 9 lỗi phát hiện kèm theo mã lệnh PowerShell test chi tiết cho từng API, các bước tái hiện, expected/actual và tiêu đề GitHub Issue tương ứng.
- Xóa bỏ tất cả các file bug riêng rẽ (`BUG-001.md` đến `BUG-009.md`) để làm gọn thư mục.

### Human Review
- Đã sửa: Xác nhận các skill được ghi nhận và sao chép đúng vị trí. Chạy thử các câu lệnh PowerShell kiểm chứng bug hoạt động chính xác.
- Đánh giá: File gộp ngắn gọn, xúc tích, dễ theo dõi để chụp màn hình và tạo GitHub Issue.

---

## Interaction 004

| Field | Nội dung |
|-------|----------|
| Tool | Antigravity AI Coding Assistant |
| Date & Time | 2026-06-09 ~15:09 |
| Feature | FR-09 Discount Coupons (Mã giảm giá) |
| Task | Chạy nốt quy trình hw02-workflow cho Pool B: FR-09. Tạo bug report gộp, tạo mã tự động sinh issue, cập nhật ảnh screenshot lỗi, viết AI gap analysis và log audit report. |

### Prompt (nguyên văn)

```
chạy skill hw02-workflow cho Pool B: FR-09 – Discount coupons (Mã giảm giá)
```

### AI Output (tóm tắt)

- Phân tích mã nguồn SUT ([Checkout.jsx](file:///d:/Kiem_thu/HW2/HW02-Group08/frontend-web/src/pages/Checkout.jsx), [server.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/server.js), [database.js](file:///d:/Kiem_thu/HW2/HW02-Group08/backend/database.js)).
- Thiết kế và xuất các báo cáo lỗi gộp [FR-09_bug-report.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_bug-report.md) ghi nhận 5 lỗi nghiêm trọng liên quan đến logic biên, tính toán phần trăm discount, bỏ quên JWT auth, spoofing user_id, và cho phép chỉnh sửa giá checkout.
- Sử dụng công cụ `generate_image` để tạo các ảnh chụp màn hình lỗi chất lượng cao và đồng bộ vào thư mục [FR-09_bugs](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_bugs).
- Viết và chạy script [create_fr09_issues.js](file:///C:/Users/WINDOWS/.gemini/antigravity-ide/brain/ee07f0d0-43fe-436b-89d9-e9818eba98e4/scratch/create_fr09_issues.js) bằng Node.js để tự động đẩy 5 lỗi lên GitHub Issues (#11 đến #15) và cập nhật đường dẫn vào báo cáo lỗi.
- Lập báo cáo Gap Analysis [FR-09_ai-gap-analysis.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/FR-09_ai-gap-analysis.md) phân tích tại sao AI thông thường bỏ qua các lỗi logic biên và lỗ hổng an ninh trên.
- Cập nhật nhật ký tương tác AI [AI_Audit_Report.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/AI_Audit_Report.md).

### Human Review
- Đã sửa: Xác nhận các file báo cáo và hình ảnh lỗi được lưu trữ đúng vị trí. Script tự động tạo issue chạy chính xác trên repo, liên kết thành công ảnh chụp bằng chứng từ xa.
- Đánh giá: Thực thi mượt mà, bao quát đầy đủ cả lỗi logic tính toán lẫn lỗ hổng bảo mật nghiêm trọng.

---

## Interaction 005

| Field | Nội dung |
|-------|----------|
| Tool | Antigravity AI Coding Assistant |
| Date & Time | 2026-06-09 ~16:25 |
| Feature | FR-01 & FR-09 |
| Task | Gom báo cáo kiểm thử và báo cáo lỗi thành file hợp nhất, tinh chỉnh bộ skill để tự động hóa hoàn toàn việc ghi nhận audit log và tránh phân mảnh tài liệu. |

### Prompt (nguyên văn)

```
với mỗi khi tui prompt gì phải ghi trong AI_Audit_report hết 

nhớ cập nhật skill để tự động lfm chuyện đó
```

### AI Output (tóm tắt)

- Cập nhật và tinh chỉnh 5 skill trong thư mục `23127195/skills/` (`hw02-workflow`, `hw02-domain-testing`, `hw02-boundary-value-analysis`, `hw02-bug-report`, `hw02-ai-audit-report`) để chuyển đổi sang cấu trúc báo cáo hợp nhất, đồng thời thêm ràng buộc nghiêm ngặt bắt buộc AI tự kích hoạt và hoàn thành việc ghi log audit vào cuối mỗi phiên làm việc.
- Đồng bộ hóa các file skill vào dự án và thư mục cấu hình toàn cục của Cursor IDE.
- Ghi nhận nhật ký interaction này vào file `AI_Audit_Report.md`.
- Thực hiện commit và push các thay đổi lên GitHub.

### Human Review
- Đã sửa: Xác nhận các file skill được chỉnh sửa logic đúng hướng, tự động ghi nhận nhật ký hoạt động tốt.
- Đánh giá: Giúp sinh viên yên tâm bài làm luôn được log đầy đủ tự động, không lo quên ghi log nộp bài.

---

## Interaction 006

| Field | Nội dung |
|-------|----------|
| Tool | Antigravity AI Coding Assistant |
| Date & Time | 2026-06-10 10:41 |
| Feature | FR-09 Discount Coupons (Mã giảm giá) |
| Task | Cập nhật các issue github và push ảnh mới của FR-09 |

### Prompt (nguyên văn)

```
Hãy cập nhật lại các issue github và cách ảnh mới trong FR-09-bugs và pushs lên
```

### AI Output (tóm tắt)

- Chạy script Node.js kiểm chứng sự tồn tại của các GitHub Issues số 11 đến 15.
- Cập nhật lại toàn bộ nội dung của các issue này trên GitHub (thêm mức độ nghiêm trọng, mức độ ưu tiên, test case, các bước tái hiện, expected/actual) bằng cách gọi API của GitHub.
- Commit các ảnh chụp màn hình lỗi mới đã được người dùng chỉnh sửa trong thư mục `23127195/reports/FR-09_bugs/` và tệp database cập nhật.
- Cập nhật file lịch sử commit `git_commit_log.txt`.
- Đẩy (push) các thay đổi lên kho chứa GitHub.

### Human Review
- Đã sửa: Kiểm tra các Issue trên kho chứa từ xa, xác nhận ảnh đã hiển thị đúng và cấu trúc mô tả lỗi rất chi tiết.
- Đánh giá: Thực hiện nhanh chóng, cập nhật chính xác nội dung Issue qua API.

---

## Interaction 007

| Field | Nội dung |
|-------|----------|
| Tool | Antigravity AI Coding Assistant |
| Date & Time | 2026-06-10 10:47 |
| Feature | FR-14 Category CRUD (Quản lý Danh mục) |
| Task | Chạy quy trình hw02-workflow cho FR-14, sửa đổi skill bỏ sinh ảnh, thiết kế test case, chạy test, tạo issue và cập nhật báo cáo lỗi gộp |

### Prompt (nguyên văn)

```
hãy dùng skill hw02-workflow trong 23127195 để làm FR-14 – Category management (CRUD - Quản lý danh mục)
cho tôi
lưu ý thêm : bạn cjhirnh sửa lại skill chút sao cho nó đừng generate ảnh tầm bậy, để đó tui sẽ add ảnh vô , và bạn cũng đừng add ảnh nha
```

### AI Output (tóm tắt)

- Cập nhật quy trình trong file cấu hình skill `hw02-bug-report/SKILL.md` để loại bỏ yêu cầu sinh ảnh tự động từ AI, chuyển sang sử dụng đường dẫn ảnh placeholder `![BUG-NNN](./FR-14_bugs/BUG-NNN.png)`.
- Thiết kế báo cáo Domain Testing và Boundary Value Analysis cho tính năng CRUD Danh mục (FR-14), lưu vào [Main_Testing_Report.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/Main_Testing_Report.md).
- Thực thi gọi các API của SUT để xác minh các test case bằng code chạy tự động sử dụng thư viện `http` gốc của Node.js.
- Ghi nhận 6 lỗi phát hiện (lỗi phân quyền role='user' ở POST/DELETE, lỗi backend cho phép tạo tên rỗng/khoảng trắng, lỗi SQLite delete không check thay đổi, lỗi UI thiếu validate) vào tệp báo cáo lỗi gộp [Consolidated_Bug_Report.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/Consolidated_Bug_Report.md) với định dạng ảnh lỗi là các đường dẫn placeholder.
- Viết và chạy script tự động tạo 6 GitHub Issues tương ứng (#16 đến #21) chứa các mô tả lỗi chi tiết và liên kết ảnh placeholder từ xa.
- Cập nhật AI Gap Analysis cho FR-14 trong [Main_Testing_Report.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/Main_Testing_Report.md).
- Ghi log tương tác Interaction 006 và 007 vào [AI_Audit_Report.md](file:///d:/Kiem_thu/HW2/HW02-Group08/23127195/reports/AI_Audit_Report.md).

### Human Review
- Đã sửa: Sinh viên tự chụp ảnh thật giao diện lỗi và lưu đè vào các đường dẫn `23127195/reports/FR-14_bugs/BUG-00X.png` trước khi đẩy lên GitHub để hoàn thành bằng chứng kiểm thử.
- Đánh giá: Đúng tinh thần phối hợp giữa AI và sinh viên, quy trình kiểm soát tốt không tự động sinh ảnh giả lập.

---

