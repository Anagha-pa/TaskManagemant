from rest_framework import serializers
from ..models import *


from rest_framework import serializers

from django.contrib.auth import get_user_model


class TaskSerializer(serializers.ModelSerializer):
    
    assigned_to = serializers.StringRelatedField()
    
    admin = serializers.StringRelatedField()
    
    worked_hours = serializers.IntegerField(write_only=True, required=False)
    
    completion_report = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        
        model = Task
        
        fields = ['id', 'title', 'description', 'created_at', 'assigned_to', 'due_date', 'admin', 'status','worked_hours', 'completion_report']
        
        read_only_fields = ['id', 'created_at', 'assigned_to', 'admin', 'title', 'description', 'due_date']

    def validate(self, data):
            
        if data.get('status') == 'completed':
            if 'worked_hours' not in data or 'completion_report' not in data:
                raise serializers.ValidationError("Worked hours and completion report are required when marking task as completed.")
        return data


class TaskCompletionReportSerializer(serializers.ModelSerializer):
    
    user = serializers.StringRelatedField()
    
    task = serializers.StringRelatedField()

    class Meta:
        model = TaskCompletionReport
        fields = ['id', 'task', 'user', 'completion_date', 'worked_hours', 'completion_report']
        read_only_fields = fields