from django.shortcuts import render
from .modules.home.py.home import data_home

# Create your views here.
def page_login(request):
    return render(request, 'auth/pages/login.html')

def dashboard(request):
    return render(request, 'home/pages/display.html', data_home())