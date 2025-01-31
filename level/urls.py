from django.urls import path
from .views import create_group, group_admin_dashboard  # นำเข้า View ที่เราจะใช้

urlpatterns = [
    path("create-group/", create_group, name="create_group"),  # URL สำหรับสร้าง Group
    path("group-admin-dashboard/", group_admin_dashboard, name="group_admin_dashboard"),
]
