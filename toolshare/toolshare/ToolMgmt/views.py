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
        form = ToolModelForm(request.POST, request.FILES)
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
        form = ToolModelForm()
        return render_to_response('ToolMgmt/register.html', {'form': form}, context)

def tool_edit(request, tool_id):
    context = RequestContext(request)
    tool = Tool.objects.get(id=tool_id)
    if request.POST:
        form = ToolModelForm(request.POST, request.FILES, instance=tool)
        if form.is_valid():
            new_tool = form.save()
            new_tool.owner = UserProfile.objects.get( user = request.user)
            new_tool.save()
            messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully created' % new_tool)
            return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': new_tool.id}))
        else:
            return render_to_response('ToolMgmt/edit.html', {'form': form}, context)
    else:
        form = ToolModelForm(instance=tool)
        return render_to_response('ToolMgmt/edit.html', {'form': form, 'tool' : tool}, context)

class ToolModelForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields= ('name', 'description', 'category', 'status', 'image', 'active')

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
