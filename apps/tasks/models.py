from django.db import models
from ..account.models import User

# Create your models here.


class Task(models.Model):
    Status_Choices = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_assigned', null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=25, choices=Status_Choices, default='pending')

    def __str__(self):
        return self.title
    
class TaskCompletionReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='completed_task', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_task_user', null=True, blank=True)
    completion_date = models.DateTimeField(auto_now_add=True)
    worked_hours = models.PositiveIntegerField(null=True, blank=True)
    completion_report = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.task.title} - {self.user.username} "
    


class DeletedTask(models.Model):
    org_id = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User,on_delete = models.CASCADE,related_name='deleted_tasks',null=True,blank=True)
    deleted_at = models.DateField(auto_now_add=True)