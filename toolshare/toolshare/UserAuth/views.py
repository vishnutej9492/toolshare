from django.views import generic
from UserAuth.forms import UserForm, UserProfileForm, UserEdit1Form
from django.views.generic.edit import FormView
from UserAuth.models import UserProfile
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pdb
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.core import validators

@login_required(login_url='/login/login')
def index(request):
    context = RequestContext(request)
    return render_to_response('UserAuth/index.html', context)

@login_required(login_url='/login/login')
def user_preferences(request):
    context = RequestContext(request)
    form = UserPreferences()
    return HttpResponse("Test")

def register(request):
    context = RequestContext(request)
    registered=False
    if request.method == 'POST':
        user_form= UserForm(data=request.POST)
        profile_form= UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            if user.password:
                user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            registered=True
    else:
        user_form= UserForm()
        profile_form= UserProfileForm()

    return render_to_response(
        'UserAuth/register.html',
        {'user_form': user_form, 'profile_form':profile_form, 'registered':registered},
        context)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['username']= username
        request.session['password']= password
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/home/')
                #return render(request, 'UserAuth/edit1.html')
            else:
                return HttpResponse("Not Successful")
        else:
            return HttpResponse("Invalid login")
    else:
        return render_to_response('UserAuth/login.html',{},context)

@login_required(login_url='/login/login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home')

@login_required(login_url='/login/login')
def user_edit1(request):
    context = RequestContext(request)
    edited1=False
    user1 = request.user
    #instill the instance in the form
    edit1_form= UserEdit1Form(instance=request.user)
    current_profile = UserProfile.objects.get(user = request.user)
    profile_form= UserProfileForm(instance = current_profile)

    if request.method == 'POST':
        edit1_form= UserEdit1Form(data=request.POST,instance = request.user)
        profile_form= UserProfileForm(data=request.POST)
        if edit1_form.is_valid() and profile_form.is_valid():
            user=edit1_form.save()
            #if user.password is not None and len(user.password) > 0:
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            edited1=True
            return HttpResponseRedirect('/home')
        else:
            print (edit1_form.errors, profile_form.errors)
    else:
        return render_to_response(
            'UserAuth/edit1.html',
            {'edit1_form':edit1_form,'profile_form':profile_form,'edited1':edited1},
            context)
        return render(request,'UserAuth/edit1.html')

@login_required(login_url='/login/')
def changepassword(request):
    changepasswordform = PasswordChangeForm(request.user,data = request.POST) 
    context = RequestContext(request)
    if request.method == 'POST':
        #pdb.set_trace()
        if changepasswordform.is_valid():
            #changepasswordform.clean()
            changepasswordform.save()
            #user.save()
            return HttpResponse("Your password has been changed")
        else:
            #return HttpResponse(changepasswordform.errors)
            raise ValidationError(changepasswordform.errors)
    else:
        return render_to_response(
                'UserAuth/changepassword.html',
                {'changepasswordform':changepasswordform},
                context)
