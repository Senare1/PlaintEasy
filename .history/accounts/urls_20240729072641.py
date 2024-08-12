from django.urls import path
from . import views

urlpatterns = [
    path('',views.log_in,name="login"),
    path('signup',views.signup,name="signup"),
    path('forgot',views.forgot,name='forgot'),

    path('profile',views.profile,name='profile')
]