from .models import ShareZone,Shed,Sharing
from UserAuth.models import UserProfile
from ToolMgmt.models import Tool
from django.db.models import Count

def GetMostUsedTool(sharezone):
    tool_list  = Sharing.objects.filter(tool__owner__sharezone = sharezone).values('tool').order_by().annotate(Count('pk'))
    finallist = [] 
    for otool in tool_list.all():
        finallist.append(Tool.objects.get(id = otool['tool']))
    if len(finallist) > 0:
        return finallist[0] 
    else:
        return None

def GetFrequentBorrower(sharezone):
    user_list = Sharing.objects.filter(tool__owner__sharezone = sharezone).values('borrower').order_by().annotate(Count('pk'))
    finallist = [] 
    for ouser in user_list.all():
        finallist.append(UserProfile.objects.get(id = ouser['borrower']))
    if len(finallist) > 0:
        return finallist[0]
    else:
        return None

def GetFrequentLender(sharezone):
    user_list = Sharing.objects.filter(tool__owner__sharezone = sharezone).values('lender').order_by().annotate(Count('pk'))
    finallist = [] 
    for ouser in user_list.all():
        finallist.append(UserProfile.objects.get(id = ouser['lender']))
    if len(finallist) > 0:
        return finallist[0]
    else:
        return None

def TotalTools(sharezone):
    tool_count = Tool.objects.filter(owner__sharezone = sharezone).count()
    return tool_count

def TotalUsers(zone):
    user_count =  UserProfile.objects.filter(sharezone = zone).count() 
    return user_count

def TotalSheds(zone):
    shed_count = Shed.objects.filter(sharezone = zone).count()
    return shed_count
