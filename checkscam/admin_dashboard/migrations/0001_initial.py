# Generated by Django 5.1.7 on 2025-03-23 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScamPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_scam', models.CharField(max_length=255, verbose_name='Tên người tố cáo')),
                ('stk_scam', models.CharField(blank=True, max_length=30, null=True, verbose_name='Số tài khoản')),
                ('sdt_scam', models.BigIntegerField(blank=True, null=True, verbose_name='Số điện thoại')),
                ('noi_dung', models.TextField(verbose_name='Nội dung tố cáo')),
                ('image', models.ImageField(blank=True, null=True, upload_to='scam_images/', verbose_name='Bằng chứng hình ảnh')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('status', models.CharField(choices=[('pending', 'Chờ duyệt'), ('approved', 'Đã duyệt'), ('rejected', 'Từ chối')], default='pending', max_length=10, verbose_name='Trạng thái')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
