from django.shortcuts import render, redirect
from django.http import HttpResponse
from sa_project import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, OrderChecklist, WorkOrder

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
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        if user.profile.role == "header":
            return redirect('qc:admin_home')
        elif user.profile.role == "staff":
            return redirect('qc:staff_home')
    else:
        return redirect('home')

@login_required
def account_logout(request):
    logout(request)
    return redirect('home')

@login_required
def admin_home(request):
    return render(request, "admin.html")

@login_required
def staff_home(request):
    return HttpResponse("staff_home")

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
        )

    elif role == "craftman":
        profile = Profile.objects.create(
            role = role,
            first_name = name,
            last_name = last_name,
        )

    return redirect('home')

def manage_order(request):
    orders = WorkOrder.objects.filter(creater=request.user)
    context = {
        "orders" : orders
    }

    return render(request, "manage_order.html",context)

def tmp_create_order(request):
    staffs = User.objects.filter(profile__role="staff")
    craftmans = Profile.objects.filter(role="craftman")
    context = {
        "staffs" : staffs,
        "craftmans" : craftmans
    }
    return render(request, "tmp_create_order.html", context)

def create_order(request):
    craftman_id = request.POST.get("craftman")
    number = request.POST.get("number")
    jewelry_size = request.POST.get("jewelry_size")
    product_size = request.POST.get("product_size")
    overall = request.POST.get("overall")
    shape = request.POST.get("shape")
    case = request.POST.get("case")
    
    print(craftman_id)
    craftman = Profile.objects.get(id=craftman_id)

    work_order = WorkOrder.objects.create(
        craftman = craftman,
        status = "didn't assign",
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

    return HttpResponse(request)
    # return redirect('qc:manage_order')