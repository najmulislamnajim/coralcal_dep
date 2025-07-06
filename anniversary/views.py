from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from anniversary.models import Anniversary
from core.models import Territory
import os, shutil
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

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
        
    if request.method == 'GET':
        try:
            territory = Territory.objects.get(territory=request.user.username)
            obj = Anniversary.objects.filter(territory=territory)
        except Exception as e:
            pass
        
        total_data = obj.count() if obj else 0
        print(total_data)
    return render(request, 'anniversary_form.html', context={"count":total_data})

@login_required
def edit_anniversary(request, anniversary_id):
    anniversary = Anniversary.objects.get(id=anniversary_id)
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        anniversary_date = request.POST.get('anniversary_date')
        new_image = request.FILES.get('anniversary_image')

        # Validate the data
        if not (dr_id and dr_name and anniversary_date):
            messages.error(request, "All fields are required.")
            return redirect('edit_anniversary', anniversary_id=anniversary_id)

        # Update the data in the database
        try:
            # Check and delete the old image if a new one is provided
            if new_image and anniversary.image:
                    if os.path.isfile(anniversary.image.path):
                        os.remove(anniversary.image.path)
            
            # Update the anniversary object
            anniversary.dr_id = dr_id
            anniversary.dr_name = dr_name
            anniversary.anniversary_date = anniversary_date
            if new_image:
                anniversary.image = new_image
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

@login_required
def anniversary_history(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page') or 1)
        per_page = int(request.GET.get("per_page") or 10)
        sort = request.GET.get("sort", "territory")
        direction = request.GET.get("direction", "asc")
        territory_id = request.user.username
        if per_page <= 0:
            per_page = 10
        try:
            anniversary_data = Anniversary.objects.filter(territory__territory=territory_id)
        except Anniversary.DoesNotExist:
            anniversary_data = None
            messages.error(request, "Anniversary data not found.")
        
        if search_query:
            anniversary_data = anniversary_data.filter(
                Q(dr_id__icontains=search_query) |
                Q(dr_name__icontains=search_query)
            )
        sort_by = sort
        if sort_by == "dr_id":
            sort_by = "dr_id"
        elif sort_by == "dr_name":
            sort_by = "dr_name"
        if direction == "desc":
            sort_by = f"-{sort_by}"
        anniversary_data = anniversary_data.order_by(sort_by)
        paginator = Paginator(anniversary_data, per_page)
        anniversary_data = paginator.get_page(page_number)
        return render(request, 'anniversary_history.html', {'data': anniversary_data, 'search_query': search_query, 'per_page': per_page, 'sort': sort, 'direction': direction})