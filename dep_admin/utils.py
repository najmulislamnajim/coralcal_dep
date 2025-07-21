from django.db.models import Q
from django.contrib.auth.models import User
from core.models import Territory, UserProfile
from anniversary.models import Anniversary
from knowledge_series.models import BookWishes
from dr_gift_catalogs.models import DrGiftCatalog

def filter_knowledge_series_data(request):
    data = BookWishes.objects.select_related('territory').all()
    # Filter based on the User's profile.
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            data = data.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            data = data.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            data = BookWishes.objects.none()
            
    # Filter Based on search query
    search_query = request.GET.get('search', '')
    if search_query:
        data = data.filter(
            Q(dr_id__icontains=search_query) |
            Q(dr_name__icontains=search_query) |
            Q(book__icontains=search_query) | 
            Q(territory__territory__icontains=search_query) |
            Q(territory__territory_name__icontains=search_query) |
            Q(territory__region_name__icontains=search_query) |
            Q(territory__zone_name__icontains=search_query)
        )
    # Sorting
    sort = request.GET.get("sort", "territory")
    direction = request.GET.get("direction", "asc")
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
    return data

def filter_anniversary_data(request):
    data = Anniversary.objects.select_related('territory')
    
    # Filter based on the User's profile.
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            data = data.filter(territory__zone_name=profile.zone_name)
        elif  profile.user_type == 'region':
            data = data.filter(territory__region_name=profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            data = Anniversary.objects.none()
    
    # Filter Based on search query
    search_query = request.GET.get('search', '')
    if search_query:
        try:
            data = data.filter(
                Q(dr_id__icontains = search_query) |
                Q(dr_name__icontains = search_query) |
                Q(anniversary_date__icontains = search_query) |
                Q(territory__territory__icontains = search_query) |
                Q(territory__territory_name__icontains = search_query) |
                Q(territory__region_name__icontains = search_query) |
                Q(territory__zone_name__icontains = search_query)
            )
        except ValueError:
            data = data.filter(
                Q(dr_id__icontains = search_query) |
                Q(dr_name__icontains = search_query) |
                Q(territory__territory__icontains = search_query) |
                Q(territory__territory_name__icontains = search_query) |
                Q(territory__region_name__icontains = search_query) |
                Q(territory__zone_name__icontains = search_query)
            )
    
    # Filter based on sort and direction.
    sort = request.GET.get("sort", "territory")
    direction = request.GET.get("direction", "asc")
    sort_by = None
    if sort == "territory":
        sort_by = "territory__territory"
    elif sort == "territory_name":
        sort_by = "territory__territory_name"
    elif sort == "region":
        sort_by = "territory__region_name"
    elif sort == "zone":
        sort_by = "territory__zone_name"
    elif sort == "dr_id":
        sort_by = "dr_id"
    elif sort == "dr_name":
        sort_by = "dr_name"
        
    if direction == "desc":
        sort_by = f"-{sort_by}"
    
    if sort_by:
        data = data.order_by(sort_by)
    return data

def filter_gift_catalogs_data(request):
    data = DrGiftCatalog.objects.select_related('territory').all()
    # Filter based on the User's profile.
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone':
            data = data.filter(territory__zone_name = profile.zone_name)
        elif profile.user_type == 'region':
            data = data.filter(territory__region_name = profile.region_name)
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            data = DrGiftCatalog.objects.none()
    
    # Filter Based on search query
    search_query = request.GET.get('search', '')
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
    
    # Soring
    sort = request.GET.get("sort", "territory")
    direction = request.GET.get("direction", "asc")
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
    
    return data