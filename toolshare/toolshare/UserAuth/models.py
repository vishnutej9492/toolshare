from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USPostalCodeField
# Create your models here.

class Tooler(User):
    add_line1 = models.CharField(verbose_name="Address Line 1",max_length = 100)
    add_line2 = models.CharField(verbose_name="Address Line 2",max_length = 100)
    zipcode = models.IntegerField(verbose_name ="Zipcode")
    #zipcode = USPostalCodeField()
    state = USStateField(choices = STATE_CHOICES)
    
