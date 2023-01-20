from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm


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
        
        

class SetPasswordForm(SetPasswordForm):
    class Meta:
        get_user_model()
        fields = ['new_password1', 'new_password2']
        
        
class PasswordResetForm(PasswordResetForm):
   def __init__(self, *args, **kwargs):
       super(PasswordResetForm, self).__init__(*args, **kwargs)
       