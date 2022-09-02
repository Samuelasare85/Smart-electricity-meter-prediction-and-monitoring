from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=False)
    meter_number = models.CharField(max_length=8, blank=False)
    date_created = models.DateField(auto_now_add=True)
    
    
