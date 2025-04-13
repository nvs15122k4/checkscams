from django.urls import path
from .views import home, pending_posts, result, approve_or_reject
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home_admin"),
    path('pending/', pending_posts, name="pending_posts"),
    path('result/<int:post_id>/', result, name="scam_result"),
    path('approve/<int:post_id>/', approve_or_reject, name="approve_or_reject"),
]
