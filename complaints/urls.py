from django.urls import path,include
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path("help/",views.help,name="help"),
    path("deposer/",views.let_plaint,name="let_plaint"),
    path("deposer/preuves",views.proof_data,name="proof_data"),
    path("plaintes/",views.my_plaints,name="my_plaints"),
    path("responses/",views.response,name="response"),
    path("responses/<int:id>/",views.delete_response,name="delete_response"),
    path("plaintes/<int:id>/",views.plaint_detail,name="plaint_detail"),

]