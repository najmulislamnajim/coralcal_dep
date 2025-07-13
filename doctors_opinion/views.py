from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DoctorOpinion, DoctorIndication
from core.models import Territory

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