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
from .forms import RegistrationForm, UpdateForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Friend_request
from django.template.loader import render_to_string
from django.http import HttpResponse
from core.models import Posts
import random


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
def profile(request, pk):
    page = 'profile'
    
    user_object = request.user
    user_profile = Profile.objects.get(user=user_object)
    
    profile = Profile.objects.get(id=pk)
    
    context = {
        'profile': profile,
        'user_profile': user_profile,
        'page': page
    }
        
    return render(request, 'users/profile.html', context)




def about_profile(request, pk):
    user_object = request.user
    user_profile = Profile.objects.get(user=user_object)
    
    profile_info = Profile.objects.get(id=pk)
    
    context = {
        'user_profile': user_profile,
        'profile_info': profile_info
    }

    return render(request, 'users/about.html', context)



@login_required(login_url='login')
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_request = Friend_request.objects.filter(from_user=request.user)
    my_friends = request.user.profile.friends.all()
    sent_to = []
    friends = []
    
    for user in my_friends:
        friend=user.friends.all()
        for f in friends:
            if f in friends:
                friend=friend.exclude(user=f.user)
        friends += friend
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_request:
        sent_to.append(se.to_user)
    
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, 'users/users_list.html', context)




@login_required(login_url='login')
def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    
    context = {'friends': friends}
    return render(request, 'users/friends_list.html', context)


# def send_friend_request(request, pk):
#     from_user = request.user
#     to_user = get_user_model().objects.get(id=pk)
#     friend_request, created = Friend_request.objects.get_or_create(from_user=from_user, to_user=to_user)
    
#     if created:
#         return HttpResponse(f'Friend request sent')
#     else:
#         return HttpResponse(f'Friend request already sent')
    
    
# def accept_friend_request(request, pk):
#     friend_request = Friend_request.objects.get(id=pk)
#     if friend_request.to_user == request.user:
#         friend_request.to_user.friends.add(friend_request.from_user)
#         friend_request.from_user.friends.add(friend_request.to_user)
#         friend_request.delete()
#         return HttpResponse(f'Friend request Accepted')
#     else:
#         return HttpResponse(f'Request not accepted')






@login_required(login_url='login')
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


def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your Password has been changed Successfully...")
            return redirect('users:login')
        
        else:
            for error in list(form.errors.vaues()):
                messages.error(request, error)
                
    else:
        form = SetPasswordForm(user)        
            
    context = {'form': form}
    return render(request, 'users/password_reset_confirm.html', context)


def password_reset_request(request):
    form = PasswordResetForm()
    
    context = {'form': form}
    return render(request, 'users/password_reset.html', context)


def passwordResetConfirm(request, uuid64, token):
    return redirect('users:home')