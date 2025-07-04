from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BookWishes, Territory 
import csv
from django.http import HttpResponse
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required

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
            return redirect('book_choice')

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
    if request.method=='GET':
        territory_id = request.user.username
        try:
            obj = BookWishes.objects.get(territory__territory=territory_id)
        except BookWishes.DoesNotExist:
            obj = None
        if obj:
            book_title = obj.book
            if book_title == '100 diagnostic dilemmas in clinical medicine':
                img = static('images/book1.jpg')
            elif book_title == '100 cases in obstetrics and gynaecology':
                img = static('images/book2.jpg')
            elif book_title == '100 cases in accute medicine':
                img = static('images/book3.jpg')
            else:
                print("No image found for the book title:", book_title)
            return render(request, 'choice.html', {'obj': obj, 'img':img})
        return render(request, 'book_choice.html')
    
@login_required
def edit_choice(request, id):
    if request.method == 'POST':
        dr_id = request.POST.get('dr_id')
        dr_name = request.POST.get('dr_name')
        selected_image = request.POST.get('selected_image')
        book_title = IMAGE_TO_BOOK.get(selected_image)

        if not (dr_id and dr_name and book_title):
            messages.error(request, "All fields are required and a book must be selected.")
            return redirect('edit_choice', id=id)

        try:
            obj = BookWishes.objects.get(id=id)
            obj.dr_id = dr_id
            obj.dr_name = dr_name
            obj.book = book_title
            obj.save()
            messages.success(request, f"Successfully updated book wish for {dr_name}.")
            if request.user.is_superuser:
                return redirect('knowledge_series')
            return redirect('book_choice')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('edit_choice', id=id)

    elif request.method == 'GET':
        try:
            obj = BookWishes.objects.get(id=id)
            book_title = obj.book
            if book_title == '100 diagnostic dilemmas in clinical medicine':
                img = static('images/book1.jpg')
            elif book_title == '100 cases in obstetrics and gynaecology':
                img = static('images/book2.jpg')
            elif book_title == '100 cases in accute medicine':
                img = static('images/book3.jpg')
            else:
                img = ''
            return render(request, 'edit_choice.html', {'obj': obj, 'img': img})
        except BookWishes.DoesNotExist:
            messages.error(request, "Wish not found.")
            if request.user.is_superuser:
                return redirect('knowledge_series')
            return redirect('book_choice')


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