from django.shortcuts import render, redirect
from django.http import HttpResponse
from sa_project import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, OrderChecklist, WorkOrder, MessageOrder
import sweetify
from datetime import datetime
import hashlib
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('qc:admin_home')
        elif request.user.profile.role == "header":
            return redirect('qc:admin_home')
        elif request.user.profile.role == "staff":
            return redirect('qc:staff_home')
    
    return render(request, "home.html")

def account_login(request):
    username = request.POST["email"]
    password = request.POST["password"]
    try :
        u_email = User.objects.get(username=username)
    except Exception as e:
        sweetify.error(request, 'อีเมลของคุณไม่ถูกต้อง', persistent='ยืนยัน')
        return redirect('home')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        if user.profile.role == "header":
            return redirect('qc:admin_home')
        elif user.profile.role == "staff":
            return redirect('qc:staff_home')
    else:
        sweetify.error(request, 'รหัสผ่านของคุณไม่ถูกต้อง', persistent='ยืนยัน')
        return redirect('home')

@login_required
def account_logout(request):
    logout(request)
    sweetify.info(request, 'logout เรียบร้อย', button='ตกลง', timer=3000)
    return redirect('home')

@login_required
def admin_home(request):
    return render(request, "admin.html")

@login_required
def staff_home(request):
    return render(request, "staff.html")

@login_required
def create_user_view(request):
    return render(request, "create_user.html")

@login_required
def create_user(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    last_name = request.POST.get("lastname")
    password = request.POST.get("password")
    role = request.POST.get("role")

    if role == "staff" or role == "header":
        try:
            user = User.objects.create_user(
                username = email,
                password = password,
                first_name = name,
                last_name = last_name,
            )
            profile = Profile.objects.create(
                role = role,
                user = user,
                first_name = name,
                last_name = last_name,
                email = email,
                password = hashlib.sha256(password.encode()).hexdigest(),
                date_joined = user.date_joined,
            )
        except Exception as e:
            sweetify.error(request, 'การสร้างข้อมูลพนักงานผิดพลาด', persistent='ยืนยัน')
            return redirect('qc:create_user_view')

    elif role == "craftsman":
        try:
            profile = Profile.objects.create(
                role = role,
                first_name = name,
                last_name = last_name,
                date_joined = datetime.now()
            )
        except Exception as e:
            sweetify.error(request, 'การสร้างข้อมูลพนักงานผิดพลาด', persistent='ยืนยัน')
            return redirect('qc:create_user_view')

    sweetify.info(request, 'สร้างข้อมูลพนักงานสำเร็จ', button='ตกลง', timer=3000)
    return redirect('home')

def manage_order(request):
    if request.user.profile.role == "header":
        orders = WorkOrder.objects.filter(creater=request.user)

        not_assigns = orders.filter(status="didn't assign")
        waitings = orders.filter(status="waiting")
        passeds = orders.filter(status="passed")
        completeds = orders.filter(status="completed")
        rejecteds = orders.filter(status="rejected")
        context = {
            "not_assigns" : not_assigns,
            "waitings" : waitings,
            "passeds" : passeds,
            "completeds" : completeds,
            "rejecteds" : rejecteds,
        }
        return render(request, "manage_order.html",context)
    
    elif request.user.profile.role == "staff":
        orders = WorkOrder.objects.filter(staff=request.user)

        waitings = orders.filter(status="waiting")
        passeds = orders.filter(status="passed")
        completeds = orders.filter(status="completed")
        rejecteds = orders.filter(status="rejected")
        context = {
            "waitings" : waitings,
            "passeds" : passeds,
            "completeds" : completeds,
            "rejecteds" : rejecteds,
        }

        return render(request, "manage_order_staff.html", context)

def tmp_create_order(request):
    craftsmans = Profile.objects.filter(role="craftsman")
    context = {
        "craftsmans" : craftsmans
    }
    return render(request, "tmp_create_order.html", context)

def create_order(request):
    craftsman_id = request.POST.get("craftsman")
    number = request.POST.get("number")
    jewelry_size = request.POST.get("jewelry_size")
    product_size = request.POST.get("product_size")
    overall = request.POST.get("overall")
    shape = request.POST.get("shape")
    case = request.POST.get("case")
    order_code = request.POST.get("order_code")
    
    craftsman = Profile.objects.get(id=craftsman_id)

    work_order = WorkOrder.objects.create(
        order_code = order_code,
        craftsman = craftsman,
        creater = request.user,
        jewelry_size = jewelry_size,
        number = number,
        overall = overall,
        product_size = product_size,
        shape = shape,
        case = case,
    )

    order_checklist = OrderChecklist.objects.create(
        work_order = work_order
    )

    work_order.order_checklist = order_checklist
    work_order.save()

    sweetify.info(request, 'สร้างออเดอร์สำเร็จ', button='ตกลง', timer=3000)
    return redirect('qc:manage_order')

def give_work_render(request, order_id):
    order = WorkOrder.objects.get(id=order_id)
    staffs = User.objects.filter(profile__role="staff")
    context = {
        "order" : order,
        "staffs" : staffs,
    }

    return render(request, 'give_work.html', context)

def give_work(request):
    
    order_id = request.POST.get("order_id")
    staff_id = request.POST.get("staff_id")
    
    order = WorkOrder.objects.get(id=order_id)
    staff = User.objects.get(id=staff_id)

    order.staff = staff
    order.status = "waiting"
    order.save()

    sweetify.info(request, 'แจกงานสำเร็จ', button='ตกลง', timer=3000)
    return redirect('qc:manage_order')

def check_order(request, order_id):
    order = WorkOrder.objects.get(id=order_id)
    context = {
        "order" : order,
    }

    return render(request, 'checklist.html', context)

def save_order(request):

    order_id = request.POST.get("order_id")
    shape = request.POST.get("shape")
    jewelry_size = request.POST.get("jewelry_size")
    product_size = request.POST.get("product_size")
    overall = request.POST.get("overall")
    number = request.POST.get("number")
    comment = request.POST.get("comment")

    order = WorkOrder.objects.get(id=order_id)
    checklist = OrderChecklist.objects.get(id=order.order_checklist.id)

    checklist.number = number
    checklist.shape = shape
    checklist.jewelry_size = jewelry_size
    checklist.product_size = product_size
    checklist.overall = overall
    checklist.comment = comment


    if (shape=="0" or jewelry_size=="0" or product_size=="0" or overall=="0" or number=="0"):
        order.status = "rejected"
        sweetify.info(request, 'ออเดอร์ไม่ผ่านการประเมิน', button='ตกลง', timer=3000)
    else:
        order.status = "passed"
        message_order = MessageOrder.objects.create(
            work_order = order
        )
        sweetify.info(request, 'ออเดอร์ผ่านการประเมิน', button='ตกลง', timer=3000)
    checklist.save()
    order.save()

    return redirect('qc:manage_order')
    
def send_message_completed(request, order_id):
    order = WorkOrder.objects.get(id=order_id)
    order.status = "completed"
    message_order = MessageOrder.objects.get(work_order=order)
    message_order.status = "sended"

    order.save()
    message_order.save()

    sweetify.info(request, 'แจ้งฝ่ายขายเรียบร้อย', button='ตกลง', timer=3000)
    
    return redirect('qc:manage_order')

def work_detail(request, order_id):
    order = WorkOrder.objects.get(id=order_id)

    context = {
        "order" : order,
    }

    return render(request, 'work_detail.html', context)