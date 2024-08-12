from django.urls import path,include
from . import views
from .views import ComplaintView

urlpatterns = [
    path("",views.home,name="home"),
    path("help/",views.help,name="help"),
    path("deposer/",views.let_plaint,name="let_plaint"),
    path("plaintes/",views.my_plaints,name="my_plaints"),

    path('deposer/', ComplaintView.as_view(), name='let_plaint'),
    path('home/', TemplateView.as_view(template_name='complaints/home.html'), name='home')
]