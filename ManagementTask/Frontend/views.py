from django.shortcuts import render
from .modules.home.py.home import home_data
from .modules.auth.py.login import login_data, login_process, logout_process
from .modules.menu.py.menu import menu_form, menu_page, menu_delete

def page_login(request):
    return render(request, 'auth/pages/login.html', login_data(request=request))

def process_login(request):
    return login_process(request)

def logout(request):
    return logout_process(request)

def not_found_404(request, exception):
    return render(request, 'template/pages/404.html')

def dashboard(request):
    return render(request, 'home/pages/display.html', home_data())

def menu(request):
    return menu_page(request)

def form_menu(request, id=None):
    return menu_form(request, id)

def delete_menu(request, id=None):
    return menu_delete(request, id)