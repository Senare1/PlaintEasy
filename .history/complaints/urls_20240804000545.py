from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("help/",views.help,name="help"),
    path("deposer/",views.let_plaint,name="let_plaint"),
    path("plaintes/",views.my_plaints,name="my_plaints"),
]