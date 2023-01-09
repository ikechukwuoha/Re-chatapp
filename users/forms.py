from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    other_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
   
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'other_name', 'last_name', 'username', 'password1', 'password2']
        
        
class UpdateForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()
        fields = []
    