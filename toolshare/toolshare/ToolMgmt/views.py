from django.shortcuts import render
from ToolMgmt.models import Tool

def index(request):
    all_tools = Tool.objects.all()
    return render(request, 'ToolMgmt/index.html', {'all_tools': all_tools})
