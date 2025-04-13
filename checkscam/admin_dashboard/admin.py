from django.contrib import admin
from .models import ScamPost

@admin.register(ScamPost)
class ScamPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_scam', 'stk_scam', 'sdt_scam', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('name_scam', 'stk_scam', 'sdt_scam')
    actions = ['approve_posts', 'reject_posts']
    def approve_posts(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "✅ Đã duyệt các bài tố cáo.")
    def reject_posts(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "❌ Đã từ chối các bài tố cáo.")
    approve_posts.short_description = "✔ Duyệt bài"
    reject_posts.short_description = "✖ Từ chối bài"
