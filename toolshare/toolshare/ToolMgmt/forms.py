from django.forms import ModelForm
from ToolMgmt.models import Tool, ToolCategory, ToolStatus
from UserAuth.models import UserProfile

class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'description', 'category', 'status']

    def register(self, request):
        newTool  = Tool(name = request.POST['name'], 
                        description = request.POST['description'],
                        active = True,
                        category = ToolCategory.objects.get(id = request.POST['category']),
                        status = ToolStatus.objects.get( id = request.POST['status']),
                        owner = UserProfile.objects.get( user = request.user)
                        )
        newTool.save()
