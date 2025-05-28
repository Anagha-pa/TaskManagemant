from django.urls import path
from .views import *

urlpatterns = [
    
    path('taskapilist/',TaskListView.as_view(), name='taskapi-list'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-completion-report/', TaskCompletionReportView.as_view(), name='task-completion-report'),
]