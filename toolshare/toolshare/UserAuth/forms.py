from django import forms
from django.contrib.auth.models import User
from UserAuth.models import UserProfile
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label='Password',max_length=16)

    class Meta:
        model= User
        fields= ('username','email','password','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields= ('add_line1','add_line2','zipcode','reminder_preferences','pickup_loc')

class UserEdit1Form(forms.ModelForm):
    class Meta:
        model = User
        fields= ('email','password','first_name','last_name')
        
    password = forms.CharField(widget=forms.PasswordInput(render_value = True),label='Password',max_length=16,required=False)

class UserPreferences(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('reminder_preferences','pickup_loc')
