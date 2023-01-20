from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('', views.registrationPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOutPage, name='logout'),
    
    # A url that links to the activate functionality
    path('activate/<uid64>/<token>', views.activate, name='activate'),
    
    # A url link that routes users to their profile page
    path('profile/<str:pk>', views.profile, name='profile'),
    path('users_list/', views.users_list, name='users_list'),
    
    path('friends_list/', views.friend_list, name='friends_list'),
    path('about', views.about_profile, name='about'),
    
    
    # Friend request routing
    #path('send_friend_request/<int:pk>', views.send_friend_request, name='sendfriendrequest'),
    #path('accept_friend_request/<int:pk>', views.accept_friend_request, name='acceptfriendrequest')
    
]