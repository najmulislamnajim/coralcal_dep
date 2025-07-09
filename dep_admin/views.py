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
from anniversary.models import Anniversary
from green_corner.models import GreenCorner

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
    folder_path = os.path.join(settings.MEDIA_ROOT, 'conference_images')
    
    if not os.path.exists(folder_path):
        messages.error(request, "No images found in this directory.")
        return redirect('gift_catalogs')
    
    # Create Excel file in memory
    excel_buffer = BytesIO()
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Gift Catalogs Data"
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Gift Choice']
    worksheet.append(headers)

    queryset = DrGiftCatalog.objects.select_related('territory')
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            queryset = queryset.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            queryset = queryset.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            queryset = DrGiftCatalog.objects.none()
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

    workbook.save(excel_buffer)
    excel_buffer.seek(0)
    
    # Create zip in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add all files from the folder
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                zip_file.write(file_path, relative_path)

        # Add the Excel file
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

@login_required
def anniversary(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page') or 1)
        per_page = int(request.GET.get("per_page") or 10)
        sort = request.GET.get("sort", "territory")
        direction = request.GET.get("direction", "asc")
        
        data = Anniversary.objects.select_related('territory').all()
        try:
            profile = request.user.userprofile
            if profile.user_type == 'zone':
                data = data.filter(territory__zone_name=profile.zone_name)
                print(profile.zone_name , "zone name")
            elif  profile.user_type == 'region':
                data = data.filter(territory__region_name=profile.region_name)
        except UserProfile.DoesNotExist:
            if not request.user.is_superuser:
                data = Anniversary.objects.none()
        if search_query:
            data = data.filter(
                Q(dr_id__icontains=search_query) |
                Q(dr_name__icontains=search_query) |
                Q(territory__territory__icontains=search_query) |
                Q(territory__territory_name__icontains=search_query) |
                Q(territory__region_name__icontains=search_query) |
                Q(territory__zone_name__icontains=search_query) | 
                Q(anniversary_date__icontains=search_query)
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
    return render(request, 'anniversary.html',{'data':page_obj, 'search_query':search_query, 'per_page':per_page, 'sort':sort, 'direction':direction}) 

@login_required 
def export_anniversary(request):
    """
    Export the Gift Catalogs data to an Excel file.
    """

    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Anniversary Data"
    
    # Define the header row
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Anniversary Date']
    worksheet.append(headers)
    
    # Populate the worksheet with data
    queryset = Anniversary.objects.select_related('territory')
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            queryset = queryset.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            queryset = queryset.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            queryset = Anniversary.objects.none()
    for obj in queryset:
        row = [
            obj.dr_id,
            obj.dr_name,
            obj.territory.territory,
            obj.territory.territory_name,
            obj.territory.region_name,
            obj.territory.zone_name,
            obj.anniversary_date.strftime('%Y-%m-%d')
        ]
        worksheet.append(row)
    
    # Save the workbook to a BytesIO object
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Create a response with the Excel file
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="anniversary_data.xlsx"'
    
    return response

@login_required 
def download_anniverysary(request):
    folder_path = os.path.join(settings.MEDIA_ROOT, 'anniversary_images')
    
    if not os.path.exists(folder_path):
        messages.error(request, "No images found in this directory.")
        return redirect('anniversary')
    
    # Create Excel file in memory
    excel_buffer = BytesIO()
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Anniversary Data"
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Anniversary Date']
    worksheet.append(headers)

    queryset = Anniversary.objects.select_related('territory')
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            queryset = queryset.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            queryset = queryset.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            queryset = Anniversary.objects.none()
    for obj in queryset:
        row = [
            obj.dr_id,
            obj.dr_name,
            obj.territory.territory,
            obj.territory.territory_name,
            obj.territory.region_name,
            obj.territory.zone_name,
            obj.anniversary_date
        ]
        worksheet.append(row)

    workbook.save(excel_buffer)
    excel_buffer.seek(0)
    
    # Create zip in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add all files from the folder
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                zip_file.write(file_path, relative_path)

        # Add the Excel file
        zip_file.writestr('anniversary_data.xlsx', excel_buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="anniversary_data_bundle.zip"'
    return response

@login_required
def green_corner(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page') or 1)
        per_page = int(request.GET.get("per_page") or 10)
        sort = request.GET.get("sort", "territory")
        direction = request.GET.get("direction", "asc")        
        
        data = GreenCorner.objects.select_related('territory').all()
        
        try:
            profile = request.user.userprofile
            if profile.user_type == 'zone':
                data = data.filter(territory__zone_name=profile.zone_name)
            elif  profile.user_type == 'region':
                data = data.filter(territory__region_name=profile.region_name)
        except UserProfile.DoesNotExist:
            if not request.user.is_superuser:
                data = GreenCorner.objects.none()
        if search_query:
            data = data.filter(
                Q(dr_id__icontains=search_query) |
                Q(dr_name__icontains=search_query) |
                Q(territory__territory__icontains=search_query) |
                Q(territory__territory_name__icontains=search_query) |
                Q(territory__region_name__icontains=search_query) |
                Q(territory__zone_name__icontains=search_query)
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
    return render(request, 'green_corner.html', {
        'data': page_obj, 'search_query': search_query, 'per_page': per_page, 'sort': sort, 'direction': direction
    })

@login_required 
def export_rgc(request):
    """
    Export the knowledge series data to an Excel file.
    """

    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Radiant Green Corner Data"
    
    # Define the header row
    headers = ['Dr. RPL ID', 'Dr. Name', 'Territory ID', 'Territory Name', 'Region', 'Zone', 'Flower Plants', 'Medicinal Plants']
    worksheet.append(headers)
    
    # Populate the worksheet with data
    queryset = GreenCorner.objects.select_related('territory')
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            queryset = queryset.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            queryset = queryset.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            queryset = GreenCorner.objects.none()
    for obj in queryset:
        flower_plants = f'{obj.first_flower_plant}, {obj.second_flower_plant}, {obj.third_flower_plant}.'
        medicinal_plants = f'{obj.first_medicinal_plant}, {obj.second_medicinal_plant}.'
        row = [
            obj.dr_id,
            obj.dr_name,
            obj.territory.territory,
            obj.territory.territory_name,
            obj.territory.region_name,
            obj.territory.zone_name,
            flower_plants,
            medicinal_plants
        ]
        worksheet.append(row)
    
    # Save the workbook to a BytesIO object
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Create a response with the Excel file
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="radiant_green_corner_data.xlsx"'
    
    return response