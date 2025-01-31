from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import GroupModel


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")  # รับ Role จากฟอร์ม

        # ตรวจสอบข้อมูล
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # สร้างผู้ใช้ใหม่
        user = CustomUser.objects.create_user(
            username=username, email=email, password=password1, role=role
        )
        user.save()

        messages.success(request, "Account created successfully.")
        login(request, user)
        return redirect("login")
    return render(request, "register.html")


@login_required
def create_group(request):
    if not request.user.is_group_admin():
        messages.error(request, "Only Group Admins can create groups.")
        return redirect("index")

    if request.method == "POST":
        group_name = request.POST.get("group_name")
        description = request.POST.get("description")

        if GroupModel.objects.filter(name=group_name).exists():
            messages.error(request, "This group name is already taken.")
        else:
            group = GroupModel.objects.create(name=group_name, description=description, created_by=request.user)
            messages.success(request, f"Group '{group.name}' created successfully!")
            return redirect("group_admin_dashboard")

    return render(request, "create_group.html")

@login_required
def group_admin_dashboard(request):
    user_groups = GroupModel.objects.filter(created_by=request.user)  # ✅ ดึงเฉพาะ Group ที่ User สร้าง
    return render(request, "group_admin_dashboard.html", {"user_groups": user_groups})
