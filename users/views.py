from django.shortcuts import render
from.forms import RegistrationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
#from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.template.loader import render_to_string
from django.http import HttpResponse


User = get_user_model()

@login_required(login_url='login')
def activateEmail(request, user, to_email):
    messages.success(request, f"Dear {user}, Please Check Your email {to_email} and click on the link to Complete your registration")


def registrationPage(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect("core:index")
    user = User
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            #login(request, user)
            #messages.success(request, f"Hello {user.get_full_name()}, Your Account has been successfully created...")
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('users:login')
        
        else:
            messages.error(request, f"Invalid Credentials,Please cross check your details and try again...")
            
    else:
        form = RegistrationForm()
    
    context = {'page': page}
    return render(request, 'users/registration.html', context)




def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("core:index")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = get_user_model().objects.get(email=email)
            
        except:
            messages.error(request, f"User does not exist...")
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            # redirect the user to the home page
            messages.success(request, f"Logged in Successfully...")
            return redirect("core:index")
            
        else:
            messages.error(request, f"Invalid Credentials...")
    
    context = {'page': page}
    return render(request, 'users/login.html', context)




@login_required(login_url='login')
def logOutPage(request):
    logout(request)
    return render(request, 'users/logout.html')






@login_required(login_url='login')
def profile_page(request, pk):
    
    context = {}
    return render(request, 'profile.html', context)