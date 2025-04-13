from django.db import models
from django.contrib.auth.models import User

class ScamPost(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
    ]
    id = models.AutoField(primary_key=True)
    name_scam = models.CharField(max_length=255, verbose_name="Tên người tố cáo")
    stk_scam = models.CharField(max_length=80, blank=True, null=True, verbose_name="Số tài khoản")
    sdt_scam = models.BigIntegerField(blank=True, null=True, verbose_name="Số điện thoại")
    noi_dung = models.TextField(verbose_name="Nội dung tố cáo")
    # image = models.ImageField(upload_to='scam_images/', blank=True, null=True, verbose_name="Bằng chứng hình ảnh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái"
    )
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name_scam} - {self.get_status_display()}"

class ScamImage(models.Model):
    scam_post = models.ForeignKey(ScamPost, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="scam_images/")
