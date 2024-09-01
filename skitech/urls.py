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
from market import views as m
from news import views as e
from mandi import views as a
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', u.landing, name = 'landing'),
    path('login/', u.login_view, name = 'login'),
    path('signup/',u.signup_view,name ='signup'),
    path('logout/',u.logout_view,name = 'logout_view'),
    path('disease/',s.disease_info, name = 'diseaseInfo'),
    path('croprecom/',s.crop_recommendation,name = 'cropRecommendation'),
    path('soilanalysis/',s.soil_analysis,name = "soilAnalysis"),
    path('recive_data/',i.receive_data,name = 'recieveData'),
    path('display_data/',i.display_data,name ='displayData'),
    path('addinventory/',n.add_inventory,name ='addinventory'),
    path('display_inventory/',n.inventory_list,name ='inventory_list'),
    path('delete/',n.delete_inventory,name ='delete'),
    path('weather/',u.weather_view,name = 'weather'),
    path('vendordash/',u.vendor_dashboard,name='vendordash'),
    path('dashboard/',u.dashboard,name='dashboard'),
    path('market/',m.market,name='market'),
    path('mandi/',m.mandi,name='mandi'),
    path('add_market_item/',m.add_market_item,name = 'add_market_item'),
    path('market_list/',m.market_list,name = 'market_list'),
    path('add_to_cart/',u.add_to_cart,name='add_to_cart'),
    path('cart/',u.cart_list,name='cart'),
    path('delete_cart/',u.remove_from_cart,name= 'remove_from_cart'),
    path('vendor_order/',m.vendor_orders,name = 'vendor_order'),
    path('order_list',u.order_list,name = 'order_list'),
    path('place_order/',u.place_order,name ='place_order'),
    path('headline_list/', e.headlines_list, name='headline_list'),
    path('msp/',a.msp,name = 'msp'),
    path('work_plan/',s.work_plan,name='work_plan')

    
]
