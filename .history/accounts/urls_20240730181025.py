from django.urls import path
from . import views

urlpatterns = [
    path('',views.log_in,name="login"),
    path('signup',views.signup,name="signup"),
    path('treated',views.treated,name='treated'),
    path('rejection',views.rejection,name='rejection'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('receiving',views.receiving,name='receiving'),
    path('statistics',views.statistics,name='statistics'),
    path('running',views.running,name='running'),
    path('chat',views.chat,name='chat'),
    path('archive',views.archive,name='archive'),
    path('logout',views.log_out,name='logout'),
    path('users',views.users,name='users'),
    path('settings',views.settings,name='settings'),
    path('profile',views.profile,name='profile')
]