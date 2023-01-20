from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from users.models import Profile
from .models import Posts
from django.contrib.auth.decorators import login_required


User = get_user_model()




@login_required(login_url='login')
def index(request):
    user_object = request.user
    user_profile = Profile.objects.get(user = user_object)
    
    profiles = Profile.objects.exclude(user=user_object)
    
    post = Posts.objects.all()
    
    context = {
        'user_profile': user_profile, 
        'posts': post, 
        'profiles': profiles,
    }
    
    return render(request, 'core/index.html', context)




@login_required(login_url='login')
def upload(request):
    
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Posts.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        
        return redirect('core:index')
    
    else:
        return redirect('core:index')