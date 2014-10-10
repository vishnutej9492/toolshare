from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ToolMgmt.models import Tool
from ToolMgmt.forms import ToolForm
from django.views.generic.edit import FormView
from UserAuth.models import UserProfile

def index(request):
    all_tools = Tool.objects.all()
    return render(request, 'ToolMgmt/index.html', {'all_tools': all_tools})

def mytools(request):
    currentprofile = UserProfile.objects.get( user = request.user)
    my_tools = Tool.objects.filter( owner = currentprofile)
    return render(request, 'ToolMgmt/mytools.html', {'my_tools': my_tools})

class RegisterTool(FormView):
    form_class = ToolForm
    template_name = 'ToolMgmt/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        form.register(request)
        return HttpResponseRedirect('/toolmgmt')


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
        return HttpResponseRedirect('/toolmgmt/' + tool_id)
