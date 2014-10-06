from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from UserAuth.forms import UserForm, UserProfileForm, UserEdit1Form
from django.views.generic.edit import FormView
from UserAuth.models import UserProfile
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

def register(request):
    context = RequestContext(request)
    registered=False
    if request.method == 'POST':
        user_form= UserForm(data=request.POST)
        profile_form= UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            registered=True
 #       else:
 #           print user_form.erorrs,profile_form.errors
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
        info= {username : password}
        request.session['info']= info
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponse("Successful")
                return render(request, 'UserAuth/login.html')
            else:
                return HttpResponse("Not Successful")
        else:
            return HttpResponse("Invalid login")
    else:
        return render_to_response('UserAuth/login.html',{},context)

def user_edit1(request):
    context = RequestContext(request)
    edited1=False
    info = request.session.get('info',None)
    user=authenticate(info.username,info.password)
    if user:
        if request.method == 'POST':
            edit1_form= UserEdit1Form(data=request.POST)
            profile_form= UserProfileForm(data=request.POST)
            if edit1_form.is_valid() and profile_form.is_valid():
                user=edit1_form.save()
                user.set_password(user.password)
                user.save()
                profile=profile_form.save(commit=False)
                profile.user=user
                profile.save()
                edited1=True
        else:
            edit1_form= UserEdit1Form()
            profile_form= UserProfileForm()

    return render_to_response(
        'UserAuth/edit1.html',
        {'edit1_form':edit1_form,'profile_form':profile_form,'edited1':edited1},
        context)
    return render(request,'UserAuth/edit1.html',{'info':info})
            
