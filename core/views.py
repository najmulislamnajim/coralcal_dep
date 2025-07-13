from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dep_admin.models import AccessControl

# Create your views here.
def home(request):
    return redirect('login')

def login_view(request):
    """
    Handle user login with territory code or admin credentials.
    """
    if request.user.is_authenticated:
        if not request.user.is_superuser and request.user.userprofile.user_type == 'territory':
            return redirect('territory_home')
        return redirect('knowledge_series')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.is_superuser and user.userprofile.user_type == 'territory':
                messages.success(request, "Login successful.")
                return redirect('territory_home')
            messages.success(request, "Login successful.")
            return redirect('knowledge_series')
        
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
    access_control = AccessControl.objects.all()
    access_control_states = {item.key:item.is_active for item in access_control}
    events = {
        'knowledge_series': {'label': 'Knowledge Series', 'url_name': 'book_choice', 'is_active': access_control_states['knowledge_series']},
        'gift_catalogs': {'label': 'Gift Catalogs', 'url_name': 'gift_choice', 'is_active': access_control_states['gift_catalogs']},
        'anniversary': {'label': 'Enlighten Together', 'url_name': 'anniversary_form', 'is_active': access_control_states['anniversary']},
        'green_corner': {'label': 'Green Corner', 'url_name': 'rgc_upload', 'is_active': access_control_states['green_corner']},
        'doctors_opinion': {'label': "Doctor's Opinion", 'url_name': 'do_form', 'is_active': access_control_states['doctors_opinion']},
    }
    return render(request, 'home.html', {'events': events})