from django.shortcuts import render, redirect
from django.http import HttpResponse
from sa_project import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def home(request):
    user = User.objects.get(id=request.user.id)
    if request.user.is_authenticated:
        if user.profile.role == "header":
            return redirect('qc:admin_home')
        elif user.profile.role == "staff":
            return redirect('qc:staff_home')
         
    return render(request, "home.html")

def account_login(request):
    username = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        if pf.role == "header":
            return redirect('qc:admin_home')
        elif pf.role == "staff":
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

    user = User.objects.create_user(
        username = email,
        password = password,
        first_name = name,
        last_name = last_name,
    )
    
    profile = Profile.objects.create(
        role = role,
        user = user
    )

    return HttpResponse(user)

def manage_order(request):
    return render(request, "manage_order.html")