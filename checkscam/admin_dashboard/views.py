from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import ScamPost

def home(request):
    scam_posts = ScamPost.objects.all()
    return render(request, "admin_dashboard/home.html", {"scam_posts": scam_posts})

def pending_posts(request):
    pending_list = ScamPost.objects.filter(status="pending")
    return render(request, "admin_dashboard/home.html", {"scam_posts": pending_list})

def result(request, post_id):
    scam = get_object_or_404(ScamPost, id=post_id)
    return render(request, "admin_dashboard/result.html", {"scam": scam})

def approve_or_reject(request, post_id):
    post = get_object_or_404(ScamPost, id=post_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            post.status = "approved"
            messages.success(request, f"✔ Đã duyệt bài: {post.name_scam}")
        elif action == "reject":
            post.status = "rejected"
            messages.error(request, f"✖ Đã từ chối bài: {post.name_scam}")
        post.save()
        return redirect("pending_posts")
    return render(request, "admin_dashboard/result.html", {"scam": post})
