from django import forms
from django.contrib.auth.models import User
from UserAuth.models import UserProfile
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label='Password',max_length=16)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password',max_length=16)
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
        fields= ('add_line1','add_line2','reminder_preferences','pickup_loc','profile_photo')
    def clean_profile_photo(self):
        profile_photo = self.cleaned_data['profile_photo']
        try:
            w, h = get_image_dimensions(profile_photo)
            #validate dimensions
            max_width = max_height = 200
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = profile_photo.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(profile_photo) > (20 * 1024):
                raise forms.ValidationError(
                    u'profile_photo file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new profile_photo
            """
            pass

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('email', 'first_name','last_name')
        
class UserPreferences(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('reminder_preferences','pickup_loc')
