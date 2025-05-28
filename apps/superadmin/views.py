from django.shortcuts import render, redirect, get_object_or_404
from ..account.validation import validate_signup_data, validate_task_data, validate_completion_report_data
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import Http404
from django.urls import reverse_lazy
from ..account.mixins import SuperAdminPermissionmixin,AdminPermissionmixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from ..account.models import User
from ..tasks.models import Task, DeletedTask, TaskCompletionReport
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, TemplateView


# Create your views here.
Users = get_user_model()

class UsercreateView(AdminPermissionmixin, View):
    template_name = 'signup.html'

    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request, *args, **kwargs):
        data = {
            'username': request.POST.get("username"),
            'password': request.POST.get("password"),
            'user_type': request.POST.get("user_type"),
        }

        errors = validate_signup_data(data)

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, self.template_name)
        
        user = User(username=data["username"])
        user.set_password(data["password"])

        if data["user_type"] == "superadmin":
            user.is_superuser = True
        elif data["user_type"] == "admin":
            user.is_staff = True

        user.save()
        messages.success(request, "User created successfully.")
        return redirect('admin-dash')
    


class UserListView(AdminPermissionmixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(user_type='superadmin').order_by('username')
    

class UserDeleteView(SuperAdminPermissionmixin, DeleteView):
    model = Users
    success_url = reverse_lazy('user-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user_type != 'user':
            raise Http404("Only regular users can be deleted.")
        return obj
    
    
class CreateAdminView(SuperAdminPermissionmixin, View):
    def get(self, request, *args, **kwargs):

        user_id = kwargs.get('pk')
        user = get_object_or_404(Users, id=user_id)

        if user.user_type == 'user':
            user.is_staff = True
            user.user_type = 'admin'
            user.save()
            return redirect('user-list')
        


class DeleteAdminView(SuperAdminPermissionmixin, View):

    def get(self, request, *args, **kwargs):
        
        user_id = kwargs.get('pk')
        user = get_object_or_404(Users, id=user_id)

        if user.user_type == 'admin':
            user.delete()
            return redirect('user-list')



class RemoveAdminView(SuperAdminPermissionmixin, View):
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        print(user)

        if user.user_type == 'admin':
            print(user.user_type, "sss")
            user.is_staff = False
            user.user_type = 'user'
            user.save()
            return redirect('user-list')
        return render(request, 'fallback_template.html')
    

@method_decorator(never_cache, name='dispatch')
class TaskCreateView(View):
    template_name = 'task_form.html'

    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()
        context = {
            'admins': User.objects.filter(user_type='admin'),
            'users': User.objects.filter(user_type='user'),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'admin': request.POST.get('admin'),
            'assigned_to': request.POST.get('assigned_to'),
            'due_date': request.POST.get('due_date'),
            'status': request.POST.get('status'),
        }

        errors = validate_task_data(data)

        if errors:
            context = {
                'errors': errors,
                'input': data,
                'admins': User.objects.filter(user_type='admin'),
                'users': User.objects.filter(user_type='user'),
            }
            return render(request, self.template_name, context)
        
        task = Task(
            title=data['title'],
            description=data['description'],
            admin_id=data['admin'],
            assigned_to_id=data['assigned_to'],
            due_date=data['due_date'],
            status=data['status'],
        )
        task.save()
        return redirect('task-list')

#
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)


class TaskPendingListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_pending.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(status__in=['pending', 'in_progress'])


class TaskCompletedListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_completedlist.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(status='completed')
    

class TaskDeletedListView(AdminPermissionmixin,LoginRequiredMixin,ListView):
    model = DeletedTask
    template_name = 'task_deleted_list.html'
    context_object_name = 'deleted_tasks'
    
    def get_queryset(self):
        
        return DeletedTask.objects.all()
    

@method_decorator(never_cache, name='dispatch')
class TaskUpdateView(AdminPermissionmixin,LoginRequiredMixin, View):
    template_name = 'task_form.html'

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        context = {
            'task': task,
            'input': {
                'title': task.title,
                'description': task.description,
                'admin': task.admin.id if task.admin else '',
                'assigned_to': task.assigned_to.id if task.assigned_to else '',
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else '',
                'status': task.status,
            },
            'admins': User.objects.filter(user_type='admin'),
            'users': User.objects.filter(user_type='user'),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)

        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'admin': request.POST.get('admin'),
            'assigned_to': request.POST.get('assigned_to'),
            'due_date': request.POST.get('due_date'),
            'status': request.POST.get('status'),
        }

        errors = validate_task_data(data)

        if errors:
            context = {
                'errors': errors,
                'input': data,
                'task': task,
                'admins': User.objects.filter(user_type='admin'),
                'users': User.objects.filter(user_type='user'),
            }
            return render(request, self.template_name, context)

        # Update task fields
        task.title = data['title']
        task.description = data['description']
        task.admin_id = data['admin']
        task.assigned_to_id = data['assigned_to']
        task.due_date = data['due_date']
        task.status = data['status']
        task.save()

        return redirect(reverse_lazy('task-list'))
    

class TaskDeleteView(AdminPermissionmixin,LoginRequiredMixin,View):
   
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(Task,id=id)
        
        data = {
            'org_id': task.id,
            'title': task.title,
            'description': task.description,
            'assigned_to': task.assigned_to,
        }
        
        DeletedTask.objects.create(**data)
        task.delete()
        return redirect('task-list')
    

class TaskProgressView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(Task, id=id)

        if task.status == 'pending':
            task.status = 'in_progress'
            task.save()
            messages.success(request, f"Task '{task.title}' status changed to In Progress.")
        else:
            messages.warning(request, "Task status cannot be updated.")

        return redirect('task-list')
        


@method_decorator(never_cache, name='dispatch')
class TaskCompletionFormView(LoginRequiredMixin, View):
    template_name = 'task_completion_form.html'

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id)
        return render(request, self.template_name, {'task': task})

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id)

        data = {
            'completion_report': request.POST.get('completion_report', '').strip()
        }

        errors = validate_completion_report_data(data)

        if errors:
            return render(request, self.template_name, {'errors': errors, 'task': task, 'input': data})

        TaskCompletionReport.objects.create(
            user=request.user,
            task=task,
            completion_report=data['completion_report']
        )

        task.status = 'completed'
        task.save()
        return redirect('task-list')


class TaskCompletionReportView(LoginRequiredMixin,View):
    
    template_name = 'task_completion_report.html'
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(TaskCompletionReport,id=id)
        return render(request, self.template_name, {'task': task})
    

class TaskCompletionReportListView(LoginRequiredMixin, View):
    template_name = 'task_completion_report.html'

    def get(self, request, *args, **kwargs):
        reports = TaskCompletionReport.objects.select_related('task', 'user').order_by('-completion_date')
        return render(request, self.template_name, {'reports': reports})

