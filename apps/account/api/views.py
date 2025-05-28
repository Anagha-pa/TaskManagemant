from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, logout
from ..validation import  validate_login_data
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import View
from django.contrib import messages
from ..models import User
from ..mixins import *

# Create your views here.
# User = get_user_model

class HomePageView(TemplateView):
    template_name = 'home.html'



@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        data = {
            'username': request.POST.get("username"),
            'password': request.POST.get("password")
        }

        errors = validate_login_data(data)

        if errors:
            return render(request, self.template_name, {"errors":errors})
        
        user = authenticate(request, username=data["username"], password=data["password"])

        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('admin-dash')
            return redirect('user-dash')
        else:
            return render(request, self.template_name, {"errors": ["Invalid username or password"]})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home-page')
    
class AdminDashboardView(AdminPermissionmixin, TemplateView):
    template_name = 'admindash.html' 

class UserDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'userdash.html'
           
        

