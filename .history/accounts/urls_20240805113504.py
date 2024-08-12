from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.login_email,name='login_email'),
    path('login_phone/',views.login_phone,name='login_phone'),

    path('signup/',views.signup,name="signup"),
    path('verify_email/',views.verify_email,name="verify_email"),
    path('regenerate_code/', views.regenerate_verification_code, name='regenerate_code'),
    
    path('treated/',views.treated,name='treated'),
    path('rejection/',views.rejection,name='rejection'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('receiving/',views.receiving,name='receiving'),
    path('complaint_detail/<int:id>/',views.complaint_detail,name='complaint_detail'),

    path('complaint_detail/detail/<int:id>/',views.reject,name='reject'),
    path('complaint_detail/detail/action/',views.action,name='action'),


    path('statistics/',views.statistics,name='statistics'),
    path('running/',views.running,name='running'),
    path('chat/',views.chat,name='chat'),
    path('logout/',views.log_out,name='logout'),


    path('users/',views.users,name='users'),
    path('users/signup_user/',views.signup_user,name="signup_user"),
    path('users/all_users/',views.all_users,name="all_users"),
    path('users/all_citozens/',views.all_citozens,name="all_citozens"),
    path('users/all_customers/',views.all_customers,name="all_customers"),
    path('users/<str:email>/',views.delete,name="delete"),

    path('user_detail/<int:id>/',views.user_detail,name='user_detail'),

    path('forgot/',views.forgot,name='forgot'),
]