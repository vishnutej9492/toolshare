from django.http import HttpResponse
from django.shortcuts import render
from ToolMgmt.models import Tool
from ToolMgmt.forms import ToolForm
from django.views.generic.edit import FormView

def index(request):
    all_tools = Tool.objects.all()
    return render(request, 'ToolMgmt/index.html', {'all_tools': all_tools})

class RegisterTool(FormView):
    form_class = ToolForm
    template_name = 'ToolMgmt/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
   
    def post(self, request,*args, **kwargs):
        form = self.form_class(initial=self.initial)
        form.register(request)
        return HttpResponse('Tool created')
def detail(request,tool_id):
	if request.method == 'GET':
		tool = Tool.objects.get(pk=tool_id)
		return render(request,'ToolMgmt/detail.html',{'tool':tool})
	else:
		return HttpResponse("Post called")

#def trigger():
	#if (Tool.active == True):
	#	Tool.active = False
	#elif (Tool.active == False):
	#	Tool.active = True

