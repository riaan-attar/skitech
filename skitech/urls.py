"""
URL configuration for skitech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as u
from soil_analysis import views as s
from iot_data import views as i
from inventory import views as n 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', u.landing, name = 'landing'),
    path('login/', u.login_view, name = 'login'),
    path('signup/',u.signup_view,name ='signup'),
    path('logout/',u.logout_view,name = 'logout_view'),
    path('disease_info/',s.disease_info, name = 'diseaseInfo'),
    path('crop_recommendation',s.crop_recommendation,name = 'cropRecommendation'),
    path('soil_analysis',s.soil_analysis,name = "soilAnalysis"),
    path('recive_data/',i.receive_data,name = 'recieveData'),
    path('display_data',i.display_data,name ='displayData'),
    path('add_inventory/',n.add_inventory,name ='addinventory'),
    path('display_inventory/',n.inventory_list,name ='inventory_list'),
    path('delete/',n.delete_inventory,name ='delete'),
    path('weather/',u.weather_view,name = 'weather'),
]
