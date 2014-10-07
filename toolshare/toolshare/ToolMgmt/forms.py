from django.forms import ModelForm
from ToolMgmt.models import Tool, ToolCategory, ToolStatus

class ToolForm(ModelForm):
    class Meta:
        model = Tool

    def register(self, request):
        newTool  = Tool(name = request.POST['name'], 
                        description = request.POST['description'],
                        active = True,
                        category = ToolCategory.objects.get(id = request.POST['category']),
                        status = ToolStatus.objects.get( id = request.POST['status'])
                        )
        newTool.save()
