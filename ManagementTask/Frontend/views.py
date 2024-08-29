from django.shortcuts import render
from .modules.home.py.home import home_data
from .modules.auth.py.login import login_data, login_process, logout_process

# Create your views here.
def page_login(request):
    return render(request, 'auth/pages/login.html', login_data(request=request))

def process_login(request):
    return login_process(request)

def logout(request):
    return logout_process(request)

def dashboard(request):
    return render(request, 'home/pages/display.html', home_data())