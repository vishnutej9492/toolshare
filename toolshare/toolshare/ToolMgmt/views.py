from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ToolMgmt.models import Tool, ToolCategory, ToolStatus
from UserAuth.models import UserProfile
from django.contrib import messages
from django import forms
from django.core.urlresolvers import reverse

def index(request):
    all_tools = Tool.objects.all()
    return render(request, 'ToolMgmt/index.html', {'all_tools': all_tools})

def mytools(request):
    my_tools = Tool.objects.filter( owner = request.user.profile)
    return render(request, 'ToolMgmt/mytools.html', {'my_tools': my_tools})

def register(request):
    if request.POST:
        form = RegisterToolForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            status = form.cleaned_data['status']

            user_profile = UserProfile.objects.get( user = request.user)
            new_tool = Tool(name=name, description=description, active=True,
                            category=category, status=status, owner = user_profile, image = request.FILES['image'])
            new_tool.save()
            messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully created' % new_tool)
            return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': new_tool.id}))
        else:
            return render(request, 'ToolMgmt/register.html',{'form' : form})
    else:
        form = RegisterToolForm()
        return render(request, 'ToolMgmt/register.html',{'form' : form})

class RegisterToolForm(forms.Form):
    error_category = {
        'required': 'You must select a category.',
        'invalid': 'Wrong selection.'
    }
    name = forms.CharField(label="Name", max_length=100)
    description = forms.CharField(label="Description", max_length=200)
    category = forms.ModelChoiceField(label="Category",queryset=ToolCategory.objects.all(), error_messages=error_category)
    status = forms.ModelChoiceField(label="Status",queryset=ToolStatus.objects.all())
    image = forms.ImageField(label="Image")

def detail(request, tool_id):
    if (request.method == 'GET'):
        tool = Tool.objects.get(pk=tool_id)
        return render(request, 'ToolMgmt/detail.html', {'tool': tool})
    else:
        tool = Tool.objects.get(pk=tool_id)
        if tool.active:
            tool.active = False
        else:
            tool.active = True
        tool.save()
        return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': tool_id}))
