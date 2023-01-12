from django.shortcuts import render
from.forms import RegistrationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
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


from .tokens import account_activation_token




def activateEmail(request, user, to_email):
    mail_subject = 'Activate Your Account'
    message = render_to_string('users/template_activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user}, Please Check Your email {to_email} and click on the link to Complete your registration")
        
    else:
        messages.error(request, f"There was a problem sending confirmation email to {to_email}. Please Check if your email is correct...")


def registrationPage(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect("core:index")
    user = get_user_model()
    
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




def activate(request, uid64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
    
        messages.success(request, f"Your email has been Confirmed, Now You can logg in and catch fun...")
        return redirect('users:login')
    else:
        messages.error(request, f"This Activation link is not valid")
        
        return redirect('users:register')
