from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DrGiftCatalog, Territory
import csv, os, shutil
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

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
        if count >=2 :
            return redirect('gift_choiced')
        return render(request, 'gift_choice.html', {
            'obj': obj,
            'count': count
        })
        
@login_required 
def view_gift_catalogs(request):
    territory_id = request.user.username
    try:
        obj = DrGiftCatalog.objects.filter(territory__territory=territory_id)
    except DrGiftCatalog.DoesNotExist:
        obj = None
        return redirect('gift_choice')   
    for item in obj:
        gift = item.gift
        if gift == 'Pureit Classic 23 L':
            item.img = static('images/pureit.webp')
        elif gift == 'Philips Blender 450W Daily Collection (HR2058/91)':
            item.img = static('images/blender.webp')
        elif gift == 'Smart Watch Fastrack Reflex Rave FX':
            item.img = static('images/watch.webp') 
        elif gift == 'Kiam Marble Coated 7 pc Set':
            item.img = static('images/cookware.jpg') 
        elif gift == 'International Scientific Conference Registration':
            item.img = static('images/conference.png')
        else:
            print('No item found')
            
    return render(request, 'view_choice.html', {'data':obj})


@login_required
def delete_gift_catalog(request, id):
    """
    Delete a gift catalog entry and its associated conference image folder if applicable.
    """
    try:
        obj = DrGiftCatalog.objects.get(id=id)

        # Check and delete the conference image folder (if gift was "Conference")
        if obj.gift == 'International Scientific Conference Registration' and obj.conference_image:
            folder_path = os.path.dirname(obj.conference_image.path)

            # Safety check to prevent deleting unintended folders
            safe_root = os.path.join(settings.MEDIA_ROOT, 'conference_images')
            if os.path.commonpath([safe_root]) == os.path.commonpath([safe_root, folder_path]):
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"Deleted folder: {folder_path}")
                else:
                    print(f"Folder not found: {folder_path}")
            else:
                print(f"Unsafe folder path skipped: {folder_path}")

        obj.delete()
        messages.success(request, "Gift catalog entry deleted successfully.")

    except DrGiftCatalog.DoesNotExist:
        messages.error(request, "Gift catalog entry not found.")
    except Exception as e:
        messages.error(request, f"Error while deleting: {str(e)}")

    return redirect('gift_choice')

@login_required
def edit_gift_catalog(request, id):
    try:
        obj = DrGiftCatalog.objects.get(id=id)
        old_gift = obj.gift 

        if request.method == 'POST':
            dr_id = request.POST.get('dr_id')
            dr_name = request.POST.get('dr_name')
            selected_image = request.POST.get('selected_image')
            conference_image = request.FILES.get('conference_image')

            if not (dr_id and dr_name and selected_image):
                messages.error(request, "All fields are required and a gift must be selected.")
                return redirect('edit_gift_catalog', id=id)

            new_gift = IMAGE_TO_GIFT.get(selected_image)

            
            if (
                old_gift == 'International Scientific Conference Registration' and 
                new_gift != 'International Scientific Conference Registration' and 
                obj.conference_image
            ):
                folder_path = os.path.dirname(obj.conference_image.path)
                safe_root = os.path.join(settings.MEDIA_ROOT, 'conference_images')

                if os.path.commonpath([safe_root]) == os.path.commonpath([safe_root, folder_path]):
                    if os.path.isdir(folder_path):
                        shutil.rmtree(folder_path)
                        print(f"[Deleted] Conference image folder: {folder_path}")
                        obj.conference_image = None  # Clean the DB field too
                    else:
                        print(f"[Skip] Folder not found: {folder_path}")
                else:
                    print(f"[Blocked] Unsafe folder path skipped: {folder_path}")

            # Update fields
            obj.dr_id = dr_id
            obj.dr_name = dr_name
            obj.gift = new_gift

            if new_gift == 'International Scientific Conference Registration' and conference_image:
                obj.conference_image = conference_image

            obj.save()
            messages.success(request, "Gift catalog entry updated successfully.")
            return redirect('gift_choiced')
        
        return render(request, 'edit_gift_choice.html', {
            'obj': obj
        })

    except DrGiftCatalog.DoesNotExist:
        messages.error(request, "Gift catalog entry not found.")
        return redirect('gift_choice')