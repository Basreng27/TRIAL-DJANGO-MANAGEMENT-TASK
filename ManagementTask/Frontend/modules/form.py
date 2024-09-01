from django import forms
from django.contrib.auth.models import User
from BackendNinja.models import Menus

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
            'password': 'Password'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': None,
        }
        
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menus
        fields = ['parent_id', 'name', 'url', 'icon', 'sequence']
        labels = {
            'parent_id': 'Parent', 
            'name': 'Name', 
            'url': 'URL', 
            'icon': 'Icon', 
            'sequence': 'Sequence'
        }
        widgets = {
            'parent_id': forms.Select(attrs={'class': 'form-control select2', 'id':'parent_id', 'style': 'width:100% !important'}), 
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'sequence': forms.NumberInput(attrs={'class': 'form-control'})
        }
        
    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        
        self.fields['parent_id'].empty_label = '--Select--'