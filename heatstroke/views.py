from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# ฟังก์ชันสำหรับหน้า Login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # หลังล็อกอินสำเร็จ ไปที่หน้า index
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # ตรวจสอบความถูกต้องของข้อมูล
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # สร้างผู้ใช้ใหม่
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully.")
        
        # ล็อกอินอัตโนมัติหลังสมัครสมาชิก
        login(request, user)
        return redirect("index")
    return render(request, "register.html")

# ฟังก์ชันสำหรับหน้า Index (ต้องล็อกอินก่อน)
@login_required
def index(request):
    return render(request, "index.html")
