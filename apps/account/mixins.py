from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse


class AdminPermissionmixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def handle_no_permission(self):
        return HttpResponse("You dont have the permission to access this page")
    

class SuperAdminPermissionmixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return HttpResponse("You dont have the permission to access this page")