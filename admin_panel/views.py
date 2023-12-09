from django.shortcuts import render, HttpResponse


# Create your views here.

def home(request):
    return render(request, 'admin_panel/index.html')
