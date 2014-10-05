from django.shortcuts import render
from ToolMgmt.models import Tool
from django.http import HttpResponse

def index(request):
    all_tools = Tool.objects.all()
    return render(request, 'ToolMgmt/index.html', {'all_tools': all_tools})

def detail(request,tool_id):
	if request.method == 'GET':
		tool = Tool.objects.get(pk=tool_id)
		return render(request,'ToolMgmt/detail.html',{'tool':tool})
	else:
		return HttpResponse("Post called")
