from django.shortcuts import render
from UserAuth.models import UserProfile
from ToolMgmt.models import Tool

# Create your views here.
def index(request):
    if(request.method == 'GET'):
        # all_tools = Tool.objects.all()
        return render(request, 'Sharing/index.html')

# def arrangement(request):
