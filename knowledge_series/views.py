from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BookWishes, Territory 
import csv
from django.http import HttpResponse

# map book names
IMAGE_TO_BOOK = {
    'image1': '100 diagnostic dilemmas in clinical medicine',
    'image2': '100 cases in obstetrics and gynaecology',
    'image3': '100 cases in accute medicine',
}

def book_choice(request):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        selected_image = request.POST.get('selected_image')

        # Map image ID to actual book title
        book_title = IMAGE_TO_BOOK.get(selected_image)

        if not (dr_id and dr_name and book_title):
            messages.error(request, "All fields are required and a book must be selected.")
            return redirect('upload')

        try:
            territory_id = request.user.username
            # Fetch the territory based on the username
            territory = Territory.objects.get(territory=territory_id)
            print(territory)
            if not territory:
                messages.error(request, "No territory found.")
                return redirect('book_choice')

            # Save data
            BookWishes.objects.create(
                territory=territory,
                dr_id=dr_id,
                dr_name=dr_name,
                book=book_title
            )
            messages.success(request, f"Successfully submitted book wish for {dr_name}.")
            return redirect('book_choice')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('book_choice')

    return render(request, 'book_choice.html')


def export_wishlist(request):
    """
    Export the book wishes to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="book_wishes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Territory', 'Territory Name', 'Region Name', 'Zone Name', 'Doctor ID', 'Doctor Name', 'Book'])

    wishes = BookWishes.objects.all()
    for wish in wishes:
        writer.writerow([wish.territory.territory, wish.territory.territory_name, wish.territory.region_name,wish.territory.zone_name, wish.dr_id, wish.dr_name, wish.book])

    return response

def admin(request):
    """
    Render the admin page with book wishes.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('login')

    wishes = BookWishes.objects.all()
    return render(request, 'admin.html', {'wishes': wishes})