from django.conf.urls import url

from . import views

app_name = "qc"

urlpatterns = [
    url(r"^admin/$", views.admin_home, name="admin_home"),
    url(r"^staff/$", views.staff_home, name="staff_home"),
    url(r"^admin/create_user$", views.create_user_view, name="create_user_view"),
    url(r"^create_user$", views.create_user, name="create_user"),
    url(r"^admin/manage_order$", views.manage_order, name="manage_order"),
    url(r"^admin/manage_order/tmp_create_order$", views.tmp_create_order, name="tmp_create_order"),
    url(r"^create_order$", views.create_order, name="create_order"),
    url(r"^staff/manage_order/(?P<order_id>[0-9]+)$", views.check_order, name="check_order"),
    url(r"^save_order$", views.save_order, name="save_order"),
    url(r"^admin/manage_order/give_work/(?P<order_id>[0-9]+)$", views.give_work_render, name="give_work_render"),
    url(r"^give_work$", views.give_work, name="give_work"),
    url(r"^send_work/(?P<order_id>[0-9]+)$", views.send_message_completed, name="send_work"),
    url(r"^admin/manage_order/work_detail/(?P<order_id>[0-9]+)$", views.work_detail, name="work_detail"),
]