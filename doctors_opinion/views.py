from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DoctorOpinion, DoctorIndication
from core.models import Territory
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@login_required
def do_form_view(request):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_address = request.POST.get('dr_address')
        dr_phone = request.POST.get('dr_phone')
        dr_specialty = request.POST.get('dr_specialty')
        indication_list = request.POST.getlist('indications[]')
        indication_list = [indication.strip() for indication in indication_list]
        
        # Validation
        if not dr_id or not dr_name or not dr_address or not dr_phone or not dr_specialty or not indication_list:
            error_message = "Please fill in all the fields."
            messages.error(request, error_message)
            return redirect('do_form')
        
        try:
            # Create a new DoctorOpinion object
            doctor_opinion = DoctorOpinion.objects.create(
                territory= Territory.objects.get(territory=request.user.username),
                dr_id = dr_id,
                dr_name = dr_name,
                dr_address = dr_address,
                dr_phone = dr_phone,
                dr_specialty = dr_specialty
            )
            for indication in indication_list:
                if indication:
                    DoctorIndication.objects.create(
                        doctor_opinion = doctor_opinion,
                        indication_text = indication
                    )
            messages.success(request, "Doctor's opinion saved successfully.")
            return redirect('do_form')
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            messages.error(request, error_message)
            return redirect('do_form')
    return render(request, 'do_form.html')


@login_required
def do_history(request):
    search_query = request.GET.get("search", "")
    sort = request.GET.get("sort", "created_at")
    direction = request.GET.get("direction", "desc")
    per_page = int(request.GET.get("per_page", 10))
    page = request.GET.get("page", 1)
    
    # sorting logic
    if direction == "desc":
        sort = f"-{sort}"
    
    doctor_opinions = DoctorOpinion.objects.filter(territory=Territory.objects.get(territory=request.user.username))
    
    #search filter
    if search_query:
        doctor_opinions = doctor_opinions.filter(
            Q(dr_id__icontains=search_query) |
            Q(dr_name__icontains=search_query) |
            Q(dr_address__icontains= search_query) |
            Q(dr_specialty__icontains=search_query) | 
            Q(dr_phone__icontains=search_query)
        )
    # sorting
    doctor_opinions = doctor_opinions.order_by(sort)
    
    # pagination
    paginator = Paginator(doctor_opinions, per_page)
    page_obj = paginator.get_page(page)
    
    context = {
        'data': page_obj,
        'search_query': search_query,
        'sort': sort,
        'direction': direction,
        'per_page': per_page,
        'page': page,
    }
    
    return render(request, 'do_history.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DoctorOpinion, DoctorIndication
from core.models import Territory  # adjust based on your project

def do_edit_view(request, pk):
    obj = get_object_or_404(DoctorOpinion, pk=pk)

    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_address = request.POST.get('dr_address')
        dr_phone = request.POST.get('dr_phone')
        dr_specialty = request.POST.get('dr_specialty')
        indications = request.POST.getlist('indications[]')

        # Update DoctorOpinion fields
        obj.dr_id = dr_id
        obj.dr_name = dr_name
        obj.dr_address = dr_address
        obj.dr_phone = dr_phone
        obj.dr_specialty = dr_specialty
        obj.save()

        # Delete existing indications and add new ones
        obj.indications.all().delete()
        for text in indications:
            cleaned_text = text.strip()
            if cleaned_text:
                DoctorIndication.objects.create(doctor_opinion=obj, indication_text=cleaned_text)

        messages.success(request, "Doctor's opinion updated successfully.")
        return redirect('do_history')

    # For GET method: pre-fill data
    existing_indications = list(obj.indications.values_list('indication_text', flat=True))
    specialties = [
        "Medicine", "GP", "Gynaecology", "Orthopedic", "Neurology", "Dentist",
        "Diabetologist", "ENT", "Surgery", "Nephro-Urology", "Cardiology",
        "Oncology", "Skin-VD", "Pediatric", "Rheumatology", "Eye", "Endocrinology", "Psychology"
    ]
    context = {
        'obj': obj,
        'indications': existing_indications,
        'specialties': specialties
    }
    return render(request, 'do_edit.html', context)
