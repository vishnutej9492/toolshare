from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from UserAuth.forms import LoginForm,RegisterForm
from django.views.generic.edit import FormView

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
            print ("Post called")
            #context = RequestContext(request)
            username = request.POST['username']
            password = request.POST['password']
            if Tooler:
                if Tooler.is_active:
                    return HttpResponse("Logged in Successfully")
                else:
                    return HttpResponse("Your account is disabled")
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
        return HttpResponse("Post Called")

