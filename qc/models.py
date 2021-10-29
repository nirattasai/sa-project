from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    class Meta:
        db_table = "users"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    ROLE = (
        ("header", "Header"),
        ("staff", "Staff"),
        ("craftman", "Craftman"),
    )
    role = models.CharField(max_length=20, choices=ROLE)

    def __str__(self):
        return "{}".format(self.user_id)

class WorkOrder(models.Model):
    class Meta:
        db_table = "work_orders"
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creater")
    STATUS = (
        ("waiting", "Waiting"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    )
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff")
    craftman = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True, blank=False)

class OrderChecklist(models.Model):
    class Meta:
        db_table = "order_checklists"
        
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    number = models.BooleanField(default=False)
    shape = models.BooleanField(default=False)
    jewelry_size = models.BooleanField(default=False)
    product_size = models.BooleanField(default=False)
    overall = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=False)