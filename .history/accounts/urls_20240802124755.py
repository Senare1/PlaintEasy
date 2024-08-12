from django.urls import path
from . import views

urlpatterns = [
    path('',views.log_in,name="login"),
    path('signup/',views.signup,name="signup"),
    
    path('treated/',views.treated,name='treated'),
    path('rejection/',views.rejection,name='rejection'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('receiving/',views.receiving,name='receiving'),
    path('statistics/',views.statistics,name='statistics'),
    path('running/',views.running,name='running'),
    path('chat/',views.chat,name='chat'),
    path('logout/',views.log_out,name='logout'),

    path('login_email/',views.login_email,name='login_email'),
    path('login_phone/',views.login_phone,name='login_phone'),

    path('users/',views.users,name='users'),
    path('users/signup_user/',views.signup_user,name="signup_user"),
    path('users/all_users/',views.all_users,name="all_users"),
    path('users/all_citozens/',views.all_citozens,name="all_citozens"),
    path('users/all_customers/',views.all_customers,name="all_customers"),
    path('users/<str:email>/',views.delete,name="delete"),

    path('settings/',views.settings,name='settings'),
    path('profile/',views.profile,name='profile')
]