from django.shortcuts import render,redirect
from .models import Doctor, Chamber
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from core.models import UserProfile
from core.utils import redirect_url
from django.urls import reverse

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
            return render(request, 'doctor_data.html')

        chamber_data = []
        for i in range(len(address)):
            if not (address[i] and phone[i] and district[i] and upazila[i] and thana[i]):
                messages.error(request, f"Please fill out all chamber fields for chamber #{i+1}.")
                return render(request, 'doctor_data.html')

            if not phone[i].startswith('01') or len(phone[i]) != 11:
                print(phone[i])
                messages.error(request, f"Invalid phone number for chamber #{i+1}. Must be 11 digits and start with '01'.")
                return render(request, 'doctor_data.html')
            

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
    return render(request, 'doctor_data.html')

@login_required
def delete_doctors_data(request, doctor_id):
    obj = get_object_or_404(Doctor, id=doctor_id)
    obj.delete()
    messages.success(request, "Doctor and associated chambers deleted successfully!")
    redirection_url = redirect_url(request, 'doctors_data', 'doctors_data', 'dd_form')
    return redirect(redirection_url)

@login_required
def edit_doctors_data(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    chambers = Chamber.objects.filter(doctor=doctor)
    if request.method == 'POST':
        dr_name = request.POST.get('dr_name')
        dr_speciality = request.POST.get('dr_speciality')
        dr_designation = request.POST.get('dr_designation')

        address = request.POST.getlist('chamber_address[]')
        phone = request.POST.getlist('chamber_phone[]')
        district = request.POST.getlist('district[]')
        upazila = request.POST.getlist('upazila[]')
        thana = request.POST.getlist('thana[]')
        chamber_data = []
        # Basic validation
        if not all([dr_name, dr_speciality, dr_designation]):
            messages.error(request, "Please fill out all required doctor fields.")
            return render(request, 'edit_doctor_data.html', {'doctor': doctor, 'chambers': chambers})
        for i in range(len(address)):
            if not (address[i] and phone[i] and district[i] and upazila[i] and thana[i]):
                messages.error(request, f"Please fill out all chamber fields for chamber #{i+1}.")
                return render(request, 'edit_doctor_data.html', {'doctor': doctor, 'chambers': chambers})
            if not phone[i].startswith('01') or len(phone[i]) != 11:
                messages.error(request, f"Invalid phone number for chamber #{i+1}. Must be 11 digits and start with '01'.")
                return render(request, 'edit_doctor_data.html', {'doctor': doctor, 'chambers': chambers})
            chamber_data.append({
                'address': address[i],
                'phone': phone[i],
                'district': district[i],
                'upazila': upazila[i],
                'thana': thana[i],
            })
        doctor.name = dr_name
        doctor.speciality = dr_speciality
        doctor.designation = dr_designation
        doctor.save()
        chambers.delete()
        for c in chamber_data:
            Chamber.objects.create(doctor=doctor, **c)
        messages.success(request, "Doctor and chambers updated successfully!")
        redirection_url = redirect_url(request, 'doctors_data', 'doctors_data', 'dd_form')
        return redirect(redirection_url)
    
    district_list = [
        "Bagerhat", "Bandarban", "Barguna", "Barisal", "Bhola", "Bogura",
        "Brahmanbaria", "Chandpur", "Chapainawabganj", "Chattogram", "Chuadanga",
        "Cox's Bazar", "Cumilla", "Dhaka", "Dinajpur", "Faridpur", "Feni",
        "Gaibandha", "Gazipur", "Gopalganj", "Habiganj", "Jamalpur", "Jashore",
        "Jhenaidah", "Joypurhat", "Khagrachhari", "Khulna", "Kishoreganj",
        "Kurigram", "Kushtia", "Lakshmipur", "Lalmonirhat", "Magura", "Manikganj",
        "Meherpur", "Moulvibazar", "Munshiganj", "Mymensingh", "Naogaon",
        "Narayanganj", "Narsingdi", "Natore", "Netrokona", "Nilphamari",
        "Noakhali", "Pabna", "Panchagarh", "Patuakhali", "Pirojpur", "Rajbari",
        "Rajshahi", "Rangamati", "Rangpur", "Satkhira", "Shariatpur", "Sherpur",
        "Sirajganj", "Sunamganj", "Sylhet", "Tangail", "Thakurgaon"
    ]
    redirection_url = redirect_url(request, 'doctors_data', 'doctors_data', 'dd_form')
    return render(request, 'edit_doctor_data.html', {'obj': doctor,'doctor': doctor, 'chambers': chambers, 'back_url':redirection_url, 'district_list': district_list})
        
