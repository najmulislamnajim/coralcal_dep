from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from anniversary.models import Anniversary
from core.models import Territory
import os, shutil
from django.conf import settings

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

@login_required
def edit_anniversary(request, anniversary_id):
    anniversary = Anniversary.objects.get(id=anniversary_id)
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        anniversary_date = request.POST.get('anniversary_date')
        anniversary_image = request.FILES.get('anniversary_image')

        # Validate the data
        if not (dr_id and dr_name and anniversary_date and anniversary_image):
            messages.error(request, "All fields are required.")
            return redirect('edit_anniversary', anniversary_id=anniversary_id)

        # Update the data in the database
        try:
            anniversary.dr_id = dr_id
            anniversary.dr_name = dr_name
            anniversary.anniversary_date = anniversary_date
            if anniversary_image:
                anniversary.image = anniversary_image
            anniversary.save()
            messages.success(request, "Anniversary data updated successfully.")
            return redirect('anniversary_form')
        except Exception as e:
            messages.error(request, f"Error updating data: {str(e)}")
            print(f"Error updating data: {str(e)}")
            return redirect('edit_anniversary', anniversary_id=anniversary_id)
    return render(request, 'edit_anniversary.html', {'anniversary': anniversary})

@login_required
def delete_anniversary(request, anniversary_id):
    try:
        anniversary = Anniversary.objects.get(id=anniversary_id)
        
        if anniversary.image:
            folder_path = os.path.dirname(anniversary.image.path)
            safe_root = os.path.join(settings.MEDIA_ROOT, 'anniversary_images')
            if os.path.commonpath([safe_root]) == os.path.commonpath([safe_root, folder_path]):
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"Deleted folder: {folder_path}")
                else:
                    print(f"Folder not found: {folder_path}")
            else:
                print(f"Unsafe folder path skipped: {folder_path}")
        anniversary.delete()
        messages.success(request, "Anniversary data deleted successfully.")
    except Anniversary.DoesNotExist:
        messages.error(request, "Anniversary data not found.")
    return redirect('anniversary_form')