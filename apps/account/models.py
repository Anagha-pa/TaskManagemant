from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    UserChoices = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User')
    )
    user_type = models.CharField(max_length=50, choices=UserChoices, default='user')

    def __str__(self):
        return self.username
