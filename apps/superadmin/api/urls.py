from django.urls import path
from .views import *

urlpatterns = [
    
    path('usercreate/', UsercreateView.as_view(), name='signup-page'),
    path('userlist/', UserListView.as_view(), name='user-list'),
    path('userdelete/<int:pk>/', UserDeleteView.as_view(), name='delete-user'),

    path('admincreate/', CreateAdminView.as_view(), name='create-admin'),
    path('admindelete/',DeleteAdminView.as_view(), name='delete-admin'),
    path('adminremove/<int:pk>/', RemoveAdminView.as_view(), name='remove-admin'),

    path('taskadd/', TaskCreateView.as_view(), name='task-add'),
    path('tasklist/', TaskListView.as_view(), name='task-list'),
    path('taskpending/',TaskPendingListView.as_view(), name='task-pending'),
    path('taskcompleted/',TaskCompletedListView.as_view(), name='task-completed'),
    path('taskdeleted/', TaskDeletedListView.as_view(), name='deleted-task'),

    path('taskupdate/<int:pk>/',TaskUpdateView.as_view(), name='task-update'),
    path('taskdelete/<int:pk>/',TaskDeleteView.as_view(), name='task-delete'),
    path('taskprogress/<int:pk>/',TaskProgressView.as_view(), name='task-progress'),
    path('taskcomplete/<int:pk>/',TaskCompletionFormView.as_view(), name='task-complete-form'),
    path('taskcompleted/<int:pk>/',TaskCompletionReportListView.as_view(), name='task-completed-report'),
    
]