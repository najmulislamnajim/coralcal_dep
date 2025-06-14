from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    return redirect('login')

def login_view(request):
    """
    Handle user login with territory code or admin credentials.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('book')
        return redirect('territory_home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.is_superuser:
                messages.success(request, "Login successful.")
                return redirect('territory_home')
            messages.success(request, "Login successful.")
            return redirect('book')
        
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login/login.html')


@login_required
def user_logout(request):
    """
    Log out the current user and redirect to login page.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def territory_home(request):
    return render(request, 'home.html')