from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username/email',max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label='Password',max_length=16)

class RegisterForm(forms.Form):
    firstname = forms.CharField(label ='First Name',max_length=100)
    lastname = forms.CharField(label ='Last Name',max_length = 100)
    email = forms.CharField(label = 'Your Email',max_length = 100)
    city = forms.CharField(label = 'City',max_length = 100)
    zipcode = forms.IntergerField(label = 'Zipcode', max_length = 6)
