from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    class Meta:
        db_table = "users"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", blank=True, null=True)
    ROLE = (
        ("header", "Header"),
        ("staff", "Staff"),
        ("craftman", "Craftman"),
    )
    role = models.CharField(max_length=20, choices=ROLE)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.user_id)

class OrderChecklist(models.Model):
    class Meta:
        db_table = "order_checklists"
        
    work_order = models.ForeignKey("WorkOrder", on_delete=models.CASCADE)
    number = models.BooleanField(default=False)
    shape = models.BooleanField(default=False)
    jewelry_size = models.BooleanField(default=False)
    product_size = models.BooleanField(default=False)
    overall = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    comment = models.TextField(default=None, blank=True, null=True)

class WorkOrder(models.Model):
    class Meta:
        db_table = "work_orders"
    order_code = models.CharField(max_length=200, null=True, blank=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creater")
    STATUS = (
        ("didn't assign", "Didn't assign"),
        ("waiting", "Waiting"),
        ("passed", "Passed"),
        ("rejected", "Rejected"),
        ("completed", "Completed")
    )
    CASE = (
        ("first_time", "First_time"),
        ("edit", "Edit")
    )
    case = models.CharField(max_length=200, choices=CASE, null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff", null=True)
    craftman = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="craftman")
    status = models.CharField(max_length=200, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    order_checklist = models.ForeignKey(OrderChecklist, on_delete=models.CASCADE, related_name="order_checklist", null=True)

    number = models.CharField(max_length=200, null=True, blank=True)
    shape = models.CharField(max_length=200, null=True, blank=True)
    jewelry_size = models.CharField(max_length=200, null=True, blank=True)
    product_size = models.CharField(max_length=200, null=True, blank=True)
    overall = models.CharField(max_length=500, null=True, blank=True)

class MessageOrder(models.Model):
    class Meta:
        db_table = "message_orders"
    STATUS = (
        ("waiting", "Waiting"),
        ("sended", "Sended")
    )

    status = models.CharField(max_length=200, choices=STATUS, default="waiting")
    created = models.DateTimeField(auto_now_add=True, blank=False)
    work_order = models.ForeignKey("WorkOrder", on_delete=models.CASCADE)