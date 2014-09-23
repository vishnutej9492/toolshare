from django.shortcuts import render
from django.http import HttpResponse
from UserAuth.models import Tooler
from django.views import generic

from django.views.generic import TemplateView
# Create your views here.
def index(request):
    return HttpResponse("This is a default login page.")

#def login(request):
    #return HttpResponse("That's it")

class LoginView(TemplateView):
    template_name = 'UserAuth/_base.html'

