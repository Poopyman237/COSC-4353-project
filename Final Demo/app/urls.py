from django.urls import path
from . import views

app_name = 'app'


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.profile_edit, name='edit_profile'),
    path('fuelhistory/', views.fuel_history, name='fuel_history'),
    path('fuelform/', views.fuel_quote, name='fuel_quote'),
    path('price_module/', views.get_price_and_total, name='price_module')
]
