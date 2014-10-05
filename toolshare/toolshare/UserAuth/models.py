from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from localflavor.us.models import USStateField
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USPostalCodeField
# Create your models here.

class UserProfile(User):
    add_line1 = models.CharField(verbose_name="Address Line 1",max_length = 100)
    add_line2 = models.CharField(verbose_name="Address Line 2",max_length = 100)
    zipcode = models.IntegerField(verbose_name ="Zipcode")
    state = USStateField(choices = STATE_CHOICES)

    def __str__(self):
        return (self.first_name + self.username)

    def Authenticate_UP(self,request): 
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(username=username, password=password)
        if user:
            if user.is_active:
                self = UserProfile.objects.get(pk=current_user.id)
                return self
            else:
                return None
        else:
            return None
