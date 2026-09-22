# CLAUDE.md

Tệp này hướng dẫn Claude Code (claude.ai/code) khi làm việc với mã nguồn trong repository này.

## Ngôn ngữ

Luôn trả lời và giải thích bằng tiếng Việt. Giữ nguyên tên lệnh, đường dẫn và đoạn code bằng tiếng Anh.

## Dự án

Đây là sandbox nhỏ để học Claude Code, không phải ứng dụng thực. Không có linter hay hệ thống build. Chỉ có git và bộ test pytest.

## Lệnh

- Chạy script: `python3 hello.py [name]` (in `Hello, <name>!`, mặc định là `World`)
- Tạo venv và cài phụ thuộc dev: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements-dev.txt`
- Chạy toàn bộ test: `.venv/bin/python -m pytest`
- Chạy một test: `.venv/bin/python -m pytest test_hello.py::test_greeting_default`

Luôn gọi pytest qua `.venv/bin/python`, không dùng `pytest` của hệ thống (máy không cài sẵn).

## CI/CD

- `.github/workflows/test.yml`: chạy `pytest` trên GitHub Actions với Python 3.10 và 3.12, khi có PR vào `main` và khi push lên `main`.
- Nhánh `main` có branch protection: PR chỉ merge được khi cả hai check CI xanh.
- Hook `.claude/hooks/pytest-on-py-edit.sh` tự chạy pytest cục bộ sau khi Claude sửa một file `.py` (cấu hình trong `.claude/settings.local.json`). Thư mục `.claude/` bị gitignore, nên hook và các luật quyền này chỉ tồn tại trên máy hiện tại, không chia sẻ qua git.

## Cấu trúc

- `hello.py`: script chỉ dùng thư viện chuẩn. `greeting(name)` trả về chuỗi chào, `main(argv)` nhận `argv` như tham số (không đọc `sys.argv` trực tiếp) để test truyền danh sách giả vào được.
- `test_hello.py`: test pytest cho `hello.py`, dùng `capsys` để bắt stdout
- `requirements-dev.txt`: phụ thuộc chỉ dùng khi phát triển (`pytest`, ghim theo major version)
- `sample.txt`: ghi chú văn bản tĩnh, không có code nào đọc đến
