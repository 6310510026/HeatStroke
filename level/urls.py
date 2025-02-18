from django.urls import path
from .views import create_group, group_admin_dashboard, view_group, add_member # นำเข้า View ที่เราจะใช้

urlpatterns = [
    path("create-group/", create_group, name="create_group"),  # URL สำหรับสร้าง Group
    path("group-admin-dashboard/", group_admin_dashboard, name="group_admin_dashboard"),
    path("group/<int:group_id>/", view_group, name="view_group"),
    path("group/<int:group_id>/add-member/", add_member, name="add_member"),
]
