from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from UserAuth.forms import LoginForm,RegisterForm
from django.views.generic.edit import FormView
from UserAuth.models import UserProfile

# Create your views here.
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'UserAuth/signin.html'
 #When page loads
    def get(self, request, *args, **kwargs):
        #return HttpResponse ("Get Called")
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
   
#When a post is called after the user submits the page.
    def post(self, request,*args, **kwargs):
            current_UP = UserProfile()
            current_UP = current_UP.Authenticate_UP(request)
            #context = RequestContext(request)
            if current_UP:
                if current_UP.is_active:
                    return HttpResponse("Logged in Successfully")
                else:
                    return HttpResponse("Your account is disabled/does not exist")
            else:
                return HttpResponse("Invalid login details supplied.")

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'UserAuth/Register.html'

    #When page loads
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})
    #When page posts
    def post(self, request, *args, **kwargs): 
        form = self.form_class(initial=self.initial)
        form.CreateUserProfile(request)
        #Get all the information from Form
        #Set all the values from RegisterForm to the Tooler Model
        #Save the Tooler Model
        return HttpResponse("User Created successfully!")
