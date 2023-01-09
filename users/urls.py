from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('', views.registrationPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOutPage, name='logout'),
    
    # A url link that routes users to their profile page
    path('profile/<str:pk>/', views.profile_page, name='profile'),
]