from django.shortcuts import render

# Create your views here.
def do_form_view(request):
    return render(request, 'do_form.html')