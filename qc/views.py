from django.shortcuts import render, redirect
from django.http import HttpResponse
from sa_project import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    print(request.user)
    if request.user.is_superuser:
        return redirect('qc:admin_home')
    elif request.user.is_staff and not request.user.is_superuser:
        return redirect('qc:staff_home')
         
    return render(request, "home.html")

def account_login(request):
    username = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        if user.is_superuser:
            return redirect('qc:admin_home')
        elif user.is_staff and not user.is_superuser:
            return redirect('qc:staff_home')
    else:
        return redirect('home')

@login_required
def account_logout(request):
    logout(request)
    return redirect('home')

def admin_home(request):
    return render(request, "admin.html")

def staff_home(request):
    return HttpResponse("staff_home")

def create_user_view(request):
    return render(request, "create_user.html")

def create_user(request):
    return None