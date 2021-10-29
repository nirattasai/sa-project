from django.conf.urls import url

from . import views

app_name = "qc"

urlpatterns = [
    url(r"^admin/$", views.admin_home, name="admin_home"),
    url(r"^staff/$", views.staff_home, name="staff_home"),
    url(r"^admin/create_user$", views.create_user_view, name="create_user_view"),
    url(r"^create_user$", views.create_user, name="create_user"),
]