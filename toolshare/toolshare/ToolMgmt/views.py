from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ToolMgmt.models import Tool, ToolCategory, ToolStatus
from UserAuth.models import UserProfile
from django.contrib import messages
from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    all_tools = Tool.objects.all()
    return render(request, 'ToolMgmt/index.html', {'all_tools': all_tools})

def mytools(request):
    my_tools = Tool.objects.filter( owner = request.user.profile)
    return render(request, 'ToolMgmt/mytools.html', {'my_tools': my_tools})

def register(request):
    context = RequestContext(request)
    if request.POST:
        form = RegisterToolModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_tool = form.save()
            new_tool.owner = UserProfile.objects.get( user = request.user)
            new_tool.actire = True
            new_tool.save()
            messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully created' % new_tool)
            return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': new_tool.id}))
        else:
            return render_to_response('ToolMgmt/register.html', {'form': form}, context)
    else:
        form = RegisterToolModelForm()
        return render_to_response('ToolMgmt/register.html', {'form': form}, context)

class RegisterToolModelForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields= ('name', 'description', 'category', 'status', 'image')

    def clean_profile_photo(self):
        image = self.cleaned_data['image']
        return image

def tool_edit(request, tool_id):
    context = RequestContext(request)
    tool = Tool.objects.get(id=tool_id)
    if request.POST:
        form = ToolEditModelForm(request.POST, request.FILES, instance=tool)
        if form.is_valid():
            new_tool = form.save()
            new_tool.owner = UserProfile.objects.get( user = request.user)
            new_tool.save()
            messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully created' % new_tool)
            return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': new_tool.id}))
        else:
            return render_to_response('ToolMgmt/edit.html', {'form': form}, context)
    else:
        form = ToolEditModelForm(instance=tool)
        return render_to_response('ToolMgmt/edit.html', {'form': form, 'tool' : tool}, context)

class ToolEditModelForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields= ('name', 'description', 'category', 'status', 'image', 'active')

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
