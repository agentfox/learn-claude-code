# CLAUDE.md

Tệp này hướng dẫn Claude Code (claude.ai/code) khi làm việc với mã nguồn trong repository này.

## Ngôn ngữ

Luôn trả lời và giải thích bằng tiếng Việt. Giữ nguyên tên lệnh, đường dẫn và đoạn code bằng tiếng Anh.

## Dự án

Đây là sandbox nhỏ để học Claude Code, không phải ứng dụng thực. Không có hệ thống build, file khai báo thư viện, linter, bộ test hay lịch sử git.

## Lệnh

- Chạy script: `python3 hello.py [name]` (in `Hello, <name>!`, mặc định là `World`)

## Cấu trúc

- `hello.py`: script độc lập chỉ dùng thư viện chuẩn (`sys.argv` để nhận tên)
- `sample.txt`: ghi chú văn bản tĩnh, không có code nào đọc đến
