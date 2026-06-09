# HW02 Agent Skills — MSSV 23127195

Bộ Agent Skills hỗ trợ làm bài **HW02 Domain Testing** trên EShop.

## Cài đặt vào Cursor

Copy toàn bộ thư mục `skills/` vào một trong hai vị trí:

```powershell
# Cá nhân (dùng mọi project)
xcopy /E /I "d:\Kiem_thu\HW2\HW02-Group08\23127195\skills\*" "%USERPROFILE%\.cursor\skills\"

# Hoặc chỉ project này
xcopy /E /I "d:\Kiem_thu\HW2\HW02-Group08\23127195\skills\*" "d:\Kiem_thu\HW2\HW02-Group08\.cursor\skills\"
```

Sau khi copy, gõ `@` trong chat Cursor và gõ tên skill (ví dụ `hw02-domain-testing`).

## Danh sách Skills

| Skill | Mục đích |
|-------|----------|
| `hw02-workflow` | Điều phối toàn bộ quy trình HW02 cho 1 feature |
| `hw02-domain-testing` | Thiết kế test case Domain Testing |
| `hw02-boundary-value-analysis` | Thiết kế test case BVA |
| `hw02-eshop-setup` | Chạy EShop, cấu hình mobile API |
| `hw02-bug-report` | Viết bug report + GitHub Issue |
| `hw02-ai-audit-report` | Ghi log AI Audit Report |

## Cách dùng nhanh

```
@hw02-workflow FR-02 Login và account lockout
```

Hoặc từng bước:

```
@hw02-domain-testing FR-01 Account registration
@hw02-boundary-value-analysis FR-01 Account registration
```

## Thư mục khác

- `templates/` — mẫu báo cáo Markdown
- `reports/` — nơi lưu báo cáo đã tạo (tự tạo khi làm bài)

## Ghi chú nộp bài

- Mỗi bước test → 1 git commit
- Bug → GitHub Issues + screenshot
- AI Audit Report → log mọi prompt/response
- AI Critique: 200–300 từ
