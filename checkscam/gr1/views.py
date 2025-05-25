from django.shortcuts import render, get_object_or_404, redirect
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import re
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from admin_dashboard.models import ScamPost, ScamImage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .serializers import GetAllPostSerializers, PostScamSerializers
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


class GetAllScamPost(APIView):
    def get(self, request):
        scam_posts = ScamPost.objects.all()
        data_scam = GetAllPostSerializers(scam_posts, many=True)
        return Response(data=data_scam.data, status=status.HTTP_200_OK)
    def post(self, request):
        mydata_scam = PostScamSerializers(data=request.data)
        if not mydata_scam.is_valid():
            return Response({'error': 'Dữ liệu không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        name_scam = mydata_scam.validated_data.get('name_scam')
        stk_scam = mydata_scam.validated_data.get('stk_scam')
        sdt_scam = mydata_scam.validated_data.get('sdt_scam')
        noi_dung = mydata_scam.validated_data.get('noi_dung')
        cs = ScamPost.objects.create(
            name_scam=name_scam,
            stk_scam=stk_scam,
            sdt_scam=sdt_scam,
            noi_dung=noi_dung
        )
        return Response({'id': cs.id}, status=status.HTTP_201_CREATED)

def home(request):
    query = request.GET.get("q")
    if query:
        scam_posts = ScamPost.objects.filter(status="approved").filter(
            stk_scam__icontains=query
        ) | ScamPost.objects.filter(
            status="approved", sdt_scam__icontains=query
        )
    else:
        scam_posts = ScamPost.objects.filter(status="approved")
    paginator = Paginator(scam_posts, 6)  
    page_number = request.GET.get("page")  
    scam_posts_page = paginator.get_page(page_number)  

    return render(request, "gr1/home.html", {"scam_posts": scam_posts_page})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(request, "gr1/login.html", {"error": "Sai tài khoản hoặc mật khẩu!"})
    return render(request, "gr1/login.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            messages.error(request, "❌ Mật khẩu không khớp!")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Tên tài khoản đã tồn tại!")
            return redirect("register")
        user = User.objects.create_user(username=username, email=email, password=password1)
        auth_login(request, user)
        messages.success(request, "✅ Đăng ký thành công!")
        return redirect("home") 
    return render(request, "gr1/register.html")

def user_logout(request):
    auth_logout(request)
    return redirect("home")

def scam_detail(request, id):
    scam = get_object_or_404(ScamPost, id=id) 
    return render(request, "gr1/detail.html", {"scam": scam})

def report(request):
    if request.method == "POST":
        name_scam = request.POST.get("name_scam")
        stk_scam = request.POST.get("stk_scam")
        sdt_scam = request.POST.get("sdt_scam")
        noi_dung = request.POST.get("noi_dung")
        scam_post = ScamPost.objects.create(
            name_scam=name_scam, stk_scam=stk_scam, sdt_scam=sdt_scam, noi_dung=noi_dung
        )
        images = request.FILES.getlist("images")
        for image in images:
            ScamImage.objects.create(scam_post=scam_post, image=image)
        return redirect("home")
    return render(request, "gr1/report.html")

genai.configure(api_key=settings.GEMINI_API_KEY)
def clean_phone_number(phone_str):
    if not phone_str or phone_str.lower() == "không có":
        return None
    cleaned = re.sub(r"\D", "", phone_str)
    return int(cleaned) if cleaned.isdigit() else None
@csrf_exempt
def fetch_gemini_scams(request):
    if request.method == "POST":
        prompt = """
        Hãy trả về JSON với danh sách 3 vụ lừa đảo phổ biến. Dữ liệu phải là JSON hợp lệ với format:
        [
            {"name": "Tên lừa đảo", "bank_account": "Số tài khoản", "phone_number": "Số điện thoại", "description": "Chi tiết vụ lừa đảo"},
            {"name": "...", "bank_account": "...", "phone_number": "...", "description": "..."},
            {"name": "...", "bank_account": "...", "phone_number": "...", "description": "..."}
        ]
        Chỉ trả về JSON, không kèm theo văn bản giải thích khác. Lưu ý: lấy thông tin thật, không phải ví dụ, hãy lấy các bài có số điện thoại hoặc số tài khoản ngân hàng (1 trong 2 hoặc cả 2), các bài không có 1 trong 2 thứ đó không lấy, lấy từ các trang báo như https://vnexpress.net, https://tuoitre.vn, https://thanhnien.vn, https://dantri.com.vn, https://vietnamnet.vn, https://zingnews.vn, https://nhandan.vn, https://laodong.vn, https://kenh14.vn, https://plo.vn.
        """
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            cleaned_text = re.sub(r"```json\n|\n```", "", response.text.strip())
            try:
                scam_data = json.loads(cleaned_text)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Dữ liệu trả về không đúng JSON", "response": response.text}, status=500)
            for item in scam_data:
                ScamPost.objects.update_or_create(
                    name_scam=item.get("name"),
                    defaults={
                        "stk_scam": item.get("bank_account"),
                        "sdt_scam": clean_phone_number(item.get("phone_number")),
                        "noi_dung": item.get("description"),
                        "status": "approved",
                    }
                )
            return JsonResponse({"message": "Dữ liệu lừa đảo Gemini đã được thêm vào!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def instructions(request):
    return render(request, "gr1/instructions.html")