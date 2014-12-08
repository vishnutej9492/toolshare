from django import forms
from django.contrib.auth.models import User
from UserAuth.models import UserProfile
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions

class UserForm(forms.ModelForm):
    regex=r'[a-zA-Z]+'
    password = forms.CharField(widget=forms.PasswordInput(),label='Password',max_length=16)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password',max_length=16)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        chars = set('0123456789')
        if any((c in chars) for c in data):
            raise forms.ValidationError("No numbers allowed in first name.")

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        chars = set('0123456789')
        if any((c in chars) for c in data):
            raise forms.ValidationError("No numbers allowed in last name.")

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    class Meta:
        model= User
        fields= ('username','email','first_name','last_name')
        

class UserProfileForm(forms.ModelForm):
    zipcode = USZipCodeField()
    class Meta:
        model = UserProfile
        fields= ('add_line1','add_line2','zipcode','reminder_preferences','pickup_loc','profile_photo')
        # fields= ('add_line1','add_line2','reminder_preferences','pickup_loc','profile_photo')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('email', 'first_name','last_name')
        
class UserPreferences(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('reminder_preferences','pickup_loc')
