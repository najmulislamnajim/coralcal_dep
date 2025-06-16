from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DrGiftCatalog, Territory
import csv 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# map gift names
IMAGE_TO_GIFT = {
    'image1': 'Pureit Classic 23 L',
    'image2': 'Philips Blender 450W Daily Collection (HR2058/91)',
    'image3': 'Smart Watch Fastrack Reflex Rave FX',
    'image4': 'Kiam Marble Coated 7 pc Set',
    'image5': 'International Scientific Conference Registration'
}
# Create your views here.
@login_required
def gift_choice(request):
    """
    Render the gift catalogs page.
    """
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        selected_image = request.POST.get('selected_image')

        if not (dr_id and dr_name and selected_image):
            messages.error(request, "All fields are required and a gift must be selected.")
            return redirect('gift_choice')
        gift = IMAGE_TO_GIFT.get(selected_image)
        conference_image = request.FILES.get('conference_image')

        try:
            territory = Territory.objects.get(territory=request.user.username)
            if not territory:
                messages.error(request, "No territory found.")
                return redirect('gift_choice')
            # Save data
            DrGiftCatalog.objects.create(
                territory=territory,
                dr_id=dr_id,
                dr_name=dr_name,
                gift=gift,
                conference_image=conference_image
            )   
            messages.success(request, f"Successfully submitted gift choice for {dr_name}.")
            return redirect('gift_choice')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('gift_choice')
    elif request.method == 'GET':
        territory_id = request.user.username
        try:
            obj = DrGiftCatalog.objects.filter(territory__territory=territory_id)
        except DrGiftCatalog.DoesNotExist:
            obj = None
        count = obj.count() if obj else 0
        return render(request, 'gift_choice.html', {
            'obj': obj,
            'count': count
        })