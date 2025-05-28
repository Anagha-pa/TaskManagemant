from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('login/', LoginView.as_view(), name='login'), 
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admindash/', AdminDashboardView.as_view(), name='admin-dash'),
    path('userdash/', UserDashboard.as_view(), name='user-dash')

]