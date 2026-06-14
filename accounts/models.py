from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Role(models.Model):
    """model class to give a role for every user and default is customer """

    #we should use OneToOneField 
    name = models.CharField(max_length=30, default='customer')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    class Meta :
        verbose_name = 'Role'
    
    def __str__(self):
        return self.user.username
        