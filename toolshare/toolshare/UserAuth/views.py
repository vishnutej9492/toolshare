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
from django.contrib import messages

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
            messages.add_message(request, messages.SUCCESS, 'Successfully registered.')
            registered=True
            return HttpResponseRedirect('/home')
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
                messages.add_message(request, messages.SUCCESS, 'Successfully logged in')
                return HttpResponseRedirect('/home/')
            else:
                messages.add_message(request, messages.ERROR, 'User is not active')
        else:
            messages.add_message(request, messages.WARNING, 'Wrong username or password')
        return HttpResponseRedirect('/home')
    else:
        return render_to_response('UserAuth/login.html',{},context)

@login_required(login_url='/login/login')
def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')
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
            messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
            return HttpResponseRedirect('/home')
        else:
            messages.add_message(request, messages.ERROR, profile_form.errors)
            return HttpResponseRedirect('/login/edit1')
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
        if changepasswordform.is_valid():
            changepasswordform.save()
            messages.add_message(request, messages.SUCCESS, 'Your password has been changed')
            return HttpResponseRedirect('/home')
        else:
            messages.add_message(request, messages.ERROR, changepasswordform.errors)
            return HttpResponseRedirect('/login/change_password')
    else:
        return render_to_response(
                'UserAuth/changepassword.html',
                {'changepasswordform':changepasswordform},
                context)
