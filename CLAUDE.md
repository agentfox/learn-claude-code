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

## Cấu trúc

- `hello.py`: script chỉ dùng thư viện chuẩn. `greeting(name)` trả về chuỗi chào, `main(argv)` nhận `argv` như tham số (không đọc `sys.argv` trực tiếp) để test truyền danh sách giả vào được.
- `test_hello.py`: test pytest cho `hello.py`, dùng `capsys` để bắt stdout
- `requirements-dev.txt`: phụ thuộc chỉ dùng khi phát triển (`pytest`)
- `sample.txt`: ghi chú văn bản tĩnh, không có code nào đọc đến
