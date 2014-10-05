from django import forms
from UserAuth.models import UserProfile
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm

class LoginForm(forms.Form):
    username = forms.CharField(label='Username/email',max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label='Password',max_length=16)

class RegisterForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['password','user','user_permissions','is_staff','is_active','is_superuser','last_login','date_joined','groups','zipcode']
    
    zipcode = USZipCodeField(max_length=5)
    password = forms.CharField(widget=forms.PasswordInput,label='Password',max_length=16)
    confirm_password = forms.CharField(widget=forms.PasswordInput,label='Confirm Password',max_length=16)

    def CreateUserProfile(self,request):
        NewUser = UserProfile()
        # Deal with all attributes of in built Django User model.
        NewUser.username = request.POST['username']
        NewUser.first_name = request.POST['first_name']
        NewUser.last_name = request.POST['last_name']
        NewUser.password = request.POST['confirm_password']
        NewUser.is_active = True
        NewUser.is_staff = False
        NewUser.is_superuser = False
        NewUser.email = request.POST['email']
        # Deal with all our attributes
        NewUser.add_line1 = request.POST['add_line1']
        NewUser.add_line1 = request.POST['add_line2']
        NewUser.zipcode = request.POST['zipcode']
        NewUser.save()
