from django.shortcuts import render

# Create your views here.
 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView
from ..permission import IsSuperadminAndAdminOnly
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from ..models import TaskCompletionReport, Task
from rest_framework.response import Response



# Create your views here.

class TaskListView(ListAPIView):
    
    authentication_classes = [JWTAuthentication]
    
    permission_classes = [IsAuthenticated]
    
    serializer_class = TaskSerializer
    
    
    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    
    
class TaskUpdateView(RetrieveUpdateAPIView):
    
    authentication_classes = [JWTAuthentication]
    
    permission_classes = [IsAuthenticated]
    
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    
    def perform_update(self, serializer):
        
        task = serializer.instance
        old_status = task.status
        new_status = serializer.validated_data.get('status')
        
        

        serializer.save()

        if new_status == 'completed':
            worked_hours = serializer.validated_data.get('worked_hours')
            completion_report = serializer.validated_data.get('completion_report')

            TaskCompletionReport.objects.create(
                task=task,
                user=self.request.user,
                worked_hours=worked_hours,
                completion_report=completion_report
            )
            
            
        
        
class TaskCompletionReportView(ListAPIView):
    
    authentication_classes = [JWTAuthentication]
    
    permission_classes = [IsSuperadminAndAdminOnly]
    
    serializer_class = TaskCompletionReportSerializer
    
    queryset = TaskCompletionReport.objects.all() 
    
    
    


    