from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from knowledge_series.models import BookWishes
from dr_gift_catalogs.models import DrGiftCatalog
from django.db.models import Q
from django.core.paginator import Paginator
import openpyxl , os, zipfile, shutil
from io import BytesIO
from django.http import HttpResponse
from core.models import Territory, UserProfile
from django.conf import settings

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def knowledge_series(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page') or 1)
        per_page = int(request.GET.get("per_page") or 10)
        sort = request.GET.get("sort", "territory")
        direction = request.GET.get("direction", "asc")        
        
        data = BookWishes.objects.select_related('territory').all()
        
        try:
            profile = request.user.userprofile
            if profile.user_type == 'zone':
                data = data.filter(territory__zone_name=profile.zone_name)
            elif  profile.user_type == 'region':
                data = data.filter(territory__region_name=profile.region_name)
        except UserProfile.DoesNotExist:
            if not request.user.is_superuser:
                data = BookWishes.objects.none()
        if search_query:
            data = data.filter(
                Q(dr_id__icontains=search_query) |
                Q(dr_name__icontains=search_query) |
                Q(territory__territory__icontains=search_query) |
                Q(territory__territory_name__icontains=search_query) |
                Q(territory__region_name__icontains=search_query) |
                Q(territory__zone_name__icontains=search_query) | 
                Q(book__icontains=search_query)
            )
        sort_by = sort
        if sort_by == "territory":
            sort_by = "territory__territory"
        elif sort_by == "territory_name":
            sort_by = "territory__territory_name"
        elif sort_by == "region":
            sort_by = "territory__region_name"
        elif sort_by == "zone":
            sort_by = "territory__zone_name"
        elif sort_by == "dr_id":
            sort_by = "dr_id"
        elif sort_by == "dr_name":
            sort_by = "dr_name"
        if direction == "desc":
            sort_by = f"-{sort_by}"
        data = data.order_by(sort_by)
        paginator = Paginator(data, per_page)
        page_obj = paginator.get_page(page_number)
    return render(request, 'knowledge_series.html', {
        'data': page_obj, 'search_query': search_query, 'per_page': per_page, 'sort': sort, 'direction': direction
    })
    
@login_required 
def export_knowledge_series(request):
    """
    Export the knowledge series data to an Excel file.
    """

    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Knowledge Series Data"
    
    # Define the header row
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Book']
    worksheet.append(headers)
    
    # Populate the worksheet with data
    queryset = BookWishes.objects.select_related('territory')
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            queryset = queryset.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            queryset = queryset.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            queryset = BookWishes.objects.none()
    for obj in queryset:
        row = [
            obj.dr_id,
            obj.dr_name,
            obj.territory.territory,
            obj.territory.territory_name,
            obj.territory.region_name,
            obj.territory.zone_name,
            obj.book
        ]
        worksheet.append(row)
    
    # Save the workbook to a BytesIO object
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Create a response with the Excel file
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="knowledge_series_data.xlsx"'
    
    return response

@login_required
def delete_knowledge_series_data(request, id):
    territory = request.user.username
    if request.user.is_superuser:
        territory = request.GET.get('territory')
    # territory_obj = Territory.objects.get(territory=territory)
    # ks_obj = BookWishes.objects.filter(territory__territory=territory)
    obj = BookWishes.objects.get(id=id)
    try:
        obj.delete()
        
        messages.success(request, f"Data deleted successfully.")
        if request.user.is_superuser:
            return redirect('knowledge_series')
        return redirect('home')
    except BookWishes.DoesNotExist:
        messages.error(request, "Invalid Item selected.")
        if request.user.is_superuser:
            return redirect('knowledge_series')
        return redirect('home')
    
@login_required 
def download_gift_catalogs(request):
    base_folder = os.path.join(settings.MEDIA_ROOT, 'conference_images')

    if not os.path.exists(base_folder):
        messages.error(request, "No images found in this directory.")
        return redirect('gift_catalogs')

    # Create Excel in memory
    excel_buffer = BytesIO()
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Gift Catalogs Data"
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Gift Choice']
    worksheet.append(headers)

    # Filter queryset
    queryset = DrGiftCatalog.objects.select_related('territory')
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            queryset = queryset.filter(territory__zone_name=profile.zone_name)
        elif profile.user_type == 'region':
            queryset = queryset.filter(territory__region_name=profile.region_name)
        elif profile.user_type == 'territory':
            queryset = queryset.filter(territory__territory=request.user.username)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            queryset = DrGiftCatalog.objects.none()

    # Collect image paths and write Excel rows
    allowed_image_paths = []
    for obj in queryset:
        # Add to Excel
        worksheet.append([
            obj.dr_id,
            obj.dr_name,
            obj.territory.territory,
            obj.territory.territory_name,
            obj.territory.region_name,
            obj.territory.zone_name,
            obj.gift
        ])

        # Include image path if it exists
        if obj.conference_image and obj.conference_image.path and os.path.exists(obj.conference_image.path):
            relative_path = os.path.relpath(obj.conference_image.path, settings.MEDIA_ROOT)
            allowed_image_paths.append(relative_path)

    workbook.save(excel_buffer)
    excel_buffer.seek(0)

    # Create ZIP
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add relevant images
        for rel_path in allowed_image_paths:
            abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
            zip_file.write(abs_path, rel_path)

        # Add Excel
        zip_file.writestr('gift_catalogs_data.xlsx', excel_buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="gift_catalogs_data_bundle.zip"'
    return response

@login_required 
def export_gift_catalogs(request):
    """
    Export the Gift Catalogs data to an Excel file.
    """

    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Gift Catalogs Data"
    
    # Define the header row
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Gift Choice']
    worksheet.append(headers)
    
    # Populate the worksheet with data
    queryset = DrGiftCatalog.objects.select_related('territory')
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            queryset = queryset.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            queryset = queryset.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            queryset = BookWishes.objects.none()
    for obj in queryset:
        row = [
            obj.dr_id,
            obj.dr_name,
            obj.territory.territory,
            obj.territory.territory_name,
            obj.territory.region_name,
            obj.territory.zone_name,
            obj.gift
        ]
        worksheet.append(row)
    
    # Save the workbook to a BytesIO object
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Create a response with the Excel file
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="gift_catalogs_data.xlsx"'
    
    return response

@login_required
def gift_catalogs(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page') or 1)
        per_page = int(request.GET.get("per_page") or 10)
        sort = request.GET.get("sort", "territory")
        direction = request.GET.get("direction", "asc")
        
        data = DrGiftCatalog.objects.select_related('territory').all()
        try:
            profile = request.user.userprofile
            if profile.user_type == 'zone':
                data = data.filter(territory__zone_name=profile.zone_name)
                print(profile.zone_name , "zone name")
            elif  profile.user_type == 'region':
                data = data.filter(territory__region_name=profile.region_name)
        except UserProfile.DoesNotExist:
            if not request.user.is_superuser:
                data = DrGiftCatalog.objects.none()
        if search_query:
            data = data.filter(
                Q(dr_id__icontains=search_query) |
                Q(dr_name__icontains=search_query) |
                Q(territory__territory__icontains=search_query) |
                Q(territory__territory_name__icontains=search_query) |
                Q(territory__region_name__icontains=search_query) |
                Q(territory__zone_name__icontains=search_query) | 
                Q(gift__icontains=search_query)
            )
        sort_by = sort
        if sort_by == "territory":
            sort_by = "territory__territory"
        elif sort_by == "territory_name":
            sort_by = "territory__territory_name"
        elif sort_by == "region":
            sort_by = "territory__region_name"
        elif sort_by == "zone":
            sort_by = "territory__zone_name"
        elif sort_by == "dr_id":
            sort_by = "dr_id"
        elif sort_by == "dr_name":
            sort_by = "dr_name"
        if direction == "desc":
            sort_by = f"-{sort_by}"
        data = data.order_by(sort_by)
        paginator = Paginator(data, per_page)
        page_obj = paginator.get_page(page_number)    
    return render(request, 'gift_catalogs.html',{'data':page_obj, 'search_query':search_query, 'per_page':per_page, 'sort':sort, 'direction':direction})           