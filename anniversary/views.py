from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from anniversary.models import Anniversary
from core.models import Territory

# Create your views here.
@login_required
def anniversary(request):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        anniversary_date = request.POST.get('anniversary_date')
        anniversary_image = request.FILES.get('anniversary_image')
        
        # Validate the data
        if not (dr_id and dr_name and anniversary_date and anniversary_image):
            messages.error(request, "All fields are required.")
            return redirect('anniversary_form')
        
        # Save the data to the database
        try:
            territory = Territory.objects.get(territory=request.user.username)
            Anniversary.objects.create(
                territory=territory,
                dr_id=dr_id,
                dr_name=dr_name,
                anniversary_date=anniversary_date,
                image=anniversary_image
            )
            messages.success(request, "Anniversary data saved successfully.")
            return redirect('anniversary_form')
        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")
            print(f"Error saving data: {str(e)}")
            return redirect('anniversary_form')
    return render(request, 'anniversary_form.html')