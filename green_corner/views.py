from django.shortcuts import render, redirect
from django.contrib import messages
from green_corner.models import GreenCorner
from core.models import Territory
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def rgc_form(request):
    if request.method == 'POST':
        territory_id = request.user
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        dr_address = request.POST.get('dr_address')
        rm_phone = request.POST.get('rm_phone')
        first_flower_plant = request.POST.get('first_flower_plant')
        second_flower_plant = request.POST.get('second_flower_plant')
        third_flower_plant = request.POST.get('third_flower_plant')
        first_medicinal_plant = request.POST.get('first_medicinal_plant')
        second_medicinal_plant = request.POST.get('second_medicinal_plant')
        
        if not dr_id or not dr_name or not dr_address or not rm_phone or not first_flower_plant or not second_flower_plant or not third_flower_plant or not first_medicinal_plant or not second_medicinal_plant:
            messages.error(request, "Please fill in all the fields.")
            redirect('rgc_upload')
        print("Received POST request with data:",territory_id, dr_id, dr_name, dr_address, rm_phone, first_flower_plant, second_flower_plant, third_flower_plant, first_medicinal_plant, second_medicinal_plant)
        try:
            territory= Territory.objects.get(territory=territory_id)
            GreenCorner.objects.create(
                territory=territory,dr_id=dr_id, dr_name=dr_name, dr_address=dr_address, rm_phone=rm_phone, first_flower_plant=first_flower_plant, second_flower_plant=second_flower_plant, third_flower_plant=third_flower_plant, first_medicinal_plant=first_medicinal_plant, second_medicinal_plant=second_medicinal_plant
            )
            messages.success(request, "Green Corner data added successfully.")
            return redirect('rgc_upload')
        except Exception as e:
            messages.error(request, "Error adding Green Corner data: " + str(e))
            print("Error adding Green Corner data: " + str(e))
            return redirect('rgc_upload')
    if request.method == 'GET':
        territory_id = request.user
        try:
            territory= Territory.objects.get(territory=territory_id)
            region_name = territory.region_name
            try:
                obj = GreenCorner.objects.get(territory=territory)
                return render(request, 'rgc_view.html', {"obj":obj})
            except GreenCorner.DoesNotExist:
                try:
                    is_exist = GreenCorner.objects.filter(
                        territory__region_name=region_name
                    ).exclude(
                        territory=territory
                    ).exists()
                    print(is_exist)
                except Exception as e:
                    print("Error fetching Green Corner data: " + str(e))
        except Exception as e:
            messages.error(request, "Error fetching Green Corner data: " + str(e))
            print("Error fetching Green Corner data: " + str(e))
            return redirect('rgc_upload')
    return render(request, 'rgc_form.html', {"is_exist":is_exist})