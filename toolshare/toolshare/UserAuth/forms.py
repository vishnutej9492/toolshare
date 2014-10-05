from django import forms
from UserAuth.models import Tooler
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm

class LoginForm(forms.Form):
    username = forms.CharField(label='Username/email',max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label='Password',max_length=16)

class RegisterForm(ModelForm):
    class Meta:
        model = Tooler
       # fields = '__all__'
        exclude = ['password','user','user_permissions','is_staff','is_active','is_superuser','last_login','date_joined','groups'] 
