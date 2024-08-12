from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("help/",views.help,name="help"),
    path("deposer/",views.let_plaint,name="let_plaint"),
    path("help/",views.help,name="help"),
]