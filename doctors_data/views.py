from django.shortcuts import render,redirect
from .models import Doctor, Chamber
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from core.models import UserProfile

# Create your views here.
def dd_form(request):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_speciality = request.POST.get('dr_speciality')
        dr_designation = request.POST.get('dr_designation')
        
        address = request.POST.getlist('chamber_address[]')
        phone = request.POST.getlist('chamber_phone[]')
        district = request.POST.getlist('district[]')
        upazila = request.POST.getlist('upazila[]')
        thana = request.POST.getlist('thana[]')

        # Basic validation
        if not all([dr_id, dr_name, dr_speciality, dr_designation]):
            messages.error(request, "Please fill out all required doctor fields.")
            return render(request, 'test.html')

        chamber_data = []
        for i in range(len(address)):
            if not (address[i] and phone[i] and district[i] and upazila[i] and thana[i]):
                messages.error(request, f"Please fill out all chamber fields for chamber #{i+1}.")
                return render(request, 'test.html')

            if not phone[i].startswith('01') or len(phone[i]) != 11:
                print(phone[i])
                messages.error(request, f"Invalid phone number for chamber #{i+1}. Must be 11 digits and start with '01'.")
                return render(request, 'test.html')
            

            chamber_data.append({
                'address': address[i],
                'phone': phone[i],
                'district': district[i],
                'upazila': upazila[i],
                'thana': thana[i],
            })

        doctor = Doctor.objects.create(
            id = dr_id,
            name = dr_name,
            speciality = dr_speciality,
            designation = dr_designation
        )
        
        for c in chamber_data:
            Chamber.objects.create(doctor=doctor, **c)

        messages.success(request, "Doctor and chambers saved successfully!")
        return redirect('dd_form')
    return render(request, 'test.html')

@login_required
def delete_doctors_data(request, doctor_id):
    obj = get_object_or_404(Doctor, id=doctor_id)
    obj.delete()
    messages.success(request, "Doctor and associated chambers deleted successfully!")
    if not request.user.is_superuser:
        try:
            profile = request.user.userprofile
            if profile.user_type == 'zone' or profile.user_type == 'region':
                return redirect('doctors_data')
            else:
                return redirect('dd_form')
        except UserProfile.DoesNotExist:
            return redirect('dd_form')
    return redirect('doctors_data')