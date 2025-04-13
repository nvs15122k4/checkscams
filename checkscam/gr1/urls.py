from django.contrib import admin
from django.urls import path
from . import views
from .views import GetAllScamPost, user_logout, user_login, user_register, fetch_gemini_scams, instructions
from admin_dashboard.models import ScamPost
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report, name='report'),
    path('register/', user_register, name='register'),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path('admin_dashboard_scampost/', GetAllScamPost.as_view()),
    path('scam/<int:id>/', views.scam_detail, name='scam_detail'),
    path('fetch-gemini-scams/', fetch_gemini_scams, name='fetch_gemini_scams'),
    path('instructions/', views.instructions, name='instructions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
