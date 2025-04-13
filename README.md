# checkscam
v2.1

❗Lưu ý: làm từ trên xuống dưới để tránh bị lỗi không mong đợi, cảm ơn.

DATABASE:
- tạo SCHEMAS tên là `checkscam` bên MYSQL.
- vào `setting` trong folder [checkscam] kéo xuống phần DATABSE để sửa mật khẩu của MYSQL.

Cài môi trường ảo
- Chạy lệnh: `python -m venv venv` tạo một môi trường ảo để cô lập các thư viện Python trong dự án.
- Chạy lệnh: `venv\Scripts\activate` kích hoạt môi trường ảo trên Windows.
- Chạy lệnh: `cd checkscam` để mở mục [checkscam].

Cài thư viện:
- Django: `pip install django` Framework chính để xây dựng web.  
- Django REST Framework: `pip install djangorestframework` Hỗ trợ API REST trong Django.  
- Google Generative AI: `pip install google-generativeai` Tích hợp AI của Google.  
- Pillow: `pip install pillow` Hỗ trợ xử lý hình ảnh trong Django.
- Requests: `pip install requests` Gửi HTTP requests trong Python.
- MySQL Client: `pip install mysqlclient` Hỗ trợ kết nối Django với MySQL.
- MySQL`pip install pymysql` Django kết nối với MySQL

Đồng bộ dữ liệu:
- Chạy lệnh:`python manage.py migrate` áp dụng các thay đổi trong cơ sở dữ liệu.
- Chạy lệnh:`python manage.py makemigrations` tạo file migration từ các thay đổi trong Models.

Tạo tài khoản admin:
- Chạy lệnh `python manage.py createsuperuser` tạo tài khoàn admin để quản lý Models.

Chạy dự án:
- Chạy lệnh: `python manage.py runserver` để chạy dự án.

Chạy AI Gemini tạo bài viết:
- Phải đăng nhập tài khoản admin.
- Vào PostMan(phải tải app PostMan mới có thể chạy api của Gemini được) chạy 'http://127.0.0.1:8000/fetch-gemini-scams/' với phương thức 'POST' để AI tạo bài viết tự động trên các trang báo

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.