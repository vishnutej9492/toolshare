from django.shortcuts import render
from django.core.urlresolvers import reverse
from UserAuth.models import UserProfile
from ToolMgmt.models import Tool
from ToolMgmt.utils import Is_Owner
from Sharing.models import Shed, ShareZone
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from .forms import ShedCreateForm, ShedEditForm
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pdb
from django.core.exceptions import ObjectDoesNotExist
from Sharing.models import Arrangement, Request, Sharing
from django import forms
from django.db.models import Q
import datetime
from django.utils.timezone import utc
from .utils import GetMostUsedTool,GetFrequentBorrower,GetFrequentLender,TotalTools,TotalUsers,TotalSheds, get_top_borrower_rating
# Create your views here.
##++++++++++++++All things related to Shed here++++++++++++++++##
@login_required(login_url='users:login')
def shedcoords(request,shed_id):
    return HttpResponse("List all shed coordinators here")

@login_required(login_url='users:login')
def shedaddcoords(request,shed_id):
    return HttpResponse("Add Shed coorinators here")

@login_required(login_url='users:login')
def sheds(request):
    profile = UserProfile.objects.get(user = request.user) 
    sharezone = ShareZone.objects.get(pk = profile.sharezone.id)
    if not Shed.objects.filter(sharezone = profile.sharezone):
        all_sheds = [] 
    else:
        all_sheds = sharezone.sheds.all()

    paginator = Paginator(all_sheds, 6)
    page = request.GET.get('page')

    try:
        paged_tools = paginator.page(page)
    except PageNotAnInteger:
        paged_tools = paginator.page(1)
    except EmptyPage:
        paged_tools = paginator.page(paginator.num_pages)

    return render(request, 'Sharing/sheds.html', {'all_sheds': paged_tools})


@login_required(login_url='users:login')
def shedcreate(request):
    context = RequestContext(request)
    profile = UserProfile.objects.get(user = request.user) 
    if request.POST:
        form = ShedCreateForm(request.POST)
        newshed = form.save(commit = False)
        newshed.sharezone = ShareZone.objects.get(zipcode = profile.sharezone.zipcode)
        newshed.save()
        newshed.coordinators.add(profile)
        newshed.save()

        messages.add_message(request,messages.SUCCESS,"Shed %s created!" %newshed)
        return HttpResponseRedirect(reverse('sharing:sheddetail',kwargs={'shed_id': newshed.id}))
    else:
        form =  ShedCreateForm()
        return render_to_response('Sharing/shedcreate.html', {'form': form}, context)


@login_required(login_url='users:login')
def sheddeactivate(request):
    return HttpResponse("Shed Deactivate")

@login_required(login_url='users:login')
def shededit(request,shed_id):
    if request.user.profile in Shed.objects.get(pk=shed_id).coordinators.all():
        print(request.user.profile.sheds.all()) 
        shed = Shed.objects.get(pk=shed_id)
        if not shed:
            return HttpRespone("No shed ")
        else:
            form = ShedEditForm()
            context = RequestContext(request)
            if request.POST:
                form = ShedEditForm(request.POST, instance = shed)
                shedchange = form.save(commit=False)
                shedchange.sharezone = request.user.profile.sharezone
                shedchange.save()
                form.save_m2m()
                messages.add_message(request,messages.SUCCESS,"Shed information changed successfully")
                return HttpResponseRedirect(reverse('sharing:sheddetail',kwargs={'shed_id':shedchange.id}))
            else:
                form = ShedEditForm(instance = shed)
                return render_to_response('Sharing/shededit.html',{'form':form,'shed':shed}, context)
    else:
        return HttpResponse("You are not authorised to view the shed or the shed does not exist at all.")

@login_required(login_url='users:login')
def sheddetail(request,shed_id):
    profile = UserProfile.objects.get(user = request.user)
    if profile in Shed.objects.get(pk=shed_id).coordinators.all():
        is_coord = True
    else:
        is_coord = False

    if request.POST:
        pass
    else:
        shed = Shed.objects.get(pk=shed_id)
        return render(request, 'Sharing/sheddetail.html', {'shed': shed,'is_coord':is_coord})

@login_required(login_url='users:login')
def tooltransfer(request,tool_id):
    tool = Tool.objects.get(pk = tool_id)
    if Is_Owner(request.user.profile , tool):
        if request.POST:
            shedid = request.POST['shed']
            if shedid:
                try:
                    shed = Shed.objects.get(pk=shedid)
                    tool.shed = shed
                    tool.save()
                    messages.add_message(request,messages.SUCCESS,"Tool transfered successfully!")
                    return HttpResponseRedirect(reverse('toolmgmt:tools'))
                except DoesNotExist:
                    raise Http404
            else:
                messages.add_message(request,messages.ERROR,"There was an error in retrieving the shed information")
                return HttpResponseRedirect(reverse('toolmgmt:tools'))
        else:
            context = RequestContext(request)
            my_sharezone = request.user.profile.sharezone
            my_sheds = my_sharezone.sheds.all()
            return render_to_response('Sharing/transfertool.html',{'mysheds':my_sheds,'tool':tool},context)
    else:
        messages.add_message(request,messages.ERROR,"You are not authorised to perform actions on this tool")
        return HttpResponseRedirect(reverse('toolmgmt:detail',kwargs = {'tool_id':tool_id}))  

@login_required(login_url='users:login')
def returntool(request,tool_id):
    tool = Tool.objects.get(pk = tool_id)
    if (tool.is_in_shed()):
        shed = tool.shed
        if shed.iscoordinator(request.user.profile):
            tool.shed = None
            tool.save()
            messages.add_message(request,messages.SUCCESS,"Tool returned successfully")
            return HttpResponseRedirect(reverse('toolmgmt:tools'))  
        else:
            messages.add_message(request,messages.ERROR,"You are not authorised to return the tool")
            return HttpResponseRedirect(reverse('toolmgmt:detail',kwargs = {'tool_id':tool_id}))  
######+++++++++++++++All things related to Shed end here+++++++++++++++#########
#######++++++++++++++All things related to search here +++++++++++++++++########
def searchtools(request):

    return HttpResponse("searchtools")


#########+++++++++++++All things related to search ends here ++++++++++++########
def create_request(request, tool_id):
    context = RequestContext(request)
    tool = Tool.objects.get(id = tool_id)
    if request.POST:
        form = RequestModelForm(request.POST)
        form.fields['start_date'].widget.attrs['id'] = 'datetimepicker'
        form.fields['end_date'].widget.attrs['id'] = 'datetimepicker2'
        if form.is_valid():
            from_date = request.POST['start_date']
            to_date = request.POST['end_date']
            if tool.is_available(from_date, to_date):
                new_request = form.save(commit=False)
                new_request.pickup_arrangement = tool.owner.pickup_loc
                new_request.borrower = request.user.profile
                new_request.lender = tool.owner
                new_request.tool = tool
                new_request.save()
                form.save_m2m()
                messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully requested to %s' % (tool, new_request.lender))
                return HttpResponseRedirect(reverse('sharing:asked-requests'))
            else:
                messages.add_message(request, messages.ERROR, 'Tool %s is not available for dates: %s to %s' % (tool, from_date, to_date))
                return render_to_response('Sharing/create_request.html', {'form': form, 'tool': tool}, context)
        else:
            return render_to_response('Sharing/create_request.html', {'form': form, 'tool': tool}, context)
    else:
        print("GET")
        form = RequestModelForm()
        form.fields['start_date'].widget.attrs['id'] = 'datetimepicker'
        form.fields['end_date'].widget.attrs['id'] = 'datetimepicker2'
        return render_to_response('Sharing/create_request.html', {'form': form, 'tool': tool}, context)

class RequestModelForm(forms.ModelForm):
    class Meta:
        model = Request
        fields= ( 'start_date', 'end_date','msg')
    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if not (isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)):
            raise forms.ValidationError("You should enter valid dates")
        if start_date > end_date:
            raise forms.ValidationError("Start date cannot be greater that end date")
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if start_date < now:
            raise forms.ValidationError("Start date cannot be lower than now")
        return self.cleaned_data

def asked_requests_index(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    waiting_requests = Request.objects.filter(borrower=request.user.profile).filter(approved=False).filter(end_date__gte=now).order_by('-start_date')
    approved_requests = Request.objects.filter(Q(borrower=request.user.profile) & Q(approved=True) &
                                               Q(end_date__gte=now) & Q(sharing__isnull=True)).order_by('-start_date')
    past_requests = Request.objects.filter(Q(borrower=request.user.profile) &
                                          (Q(end_date__lt=now) | Q(sharing__isnull=False))).order_by('-start_date')
    return render(request, 'Sharing/asked_requests_index.html', {'approved_requests': approved_requests, 'waiting_requests': waiting_requests, 'past_requests': past_requests})

def received_requests_index(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    waiting_requests = request.user.profile.waiting_received_requests()
    approved_requests = request.user.profile.approved_received_requests()
    past_requests = request.user.profile.past_received_requests()
    return render(request, 'Sharing/received_requests_index.html', {'approved_requests': approved_requests, 'waiting_requests': waiting_requests, 'past_requests': past_requests})

def received_requests_coordinator_index(request):
    sheds = request.user.profile.sheds
    return render(request, 'Sharing/received_requests_coordinator_index.html', {'sheds' : sheds})

def asked_request_detail(request, tool_request_id):
    tool_request = Request.objects.get(id = tool_request_id )
    return render(request, 'Sharing/asked_request_detail.html', {'tool_request': tool_request})

def asked_request_edit(request, tool_request_id):
    context = RequestContext(request)
    tool_request = Request.objects.get(id = tool_request_id)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    if(tool_request.borrower == request.user.profile and tool_request.approved == False and tool_request.sharing==None and tool_request.end_date > now):
        if request.POST:
            form = RequestModelForm(request.POST, request.FILES, instance=tool_request)
            if form.is_valid():
                new_tool_request = form.save()
                new_tool_request.save()
                messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully edited' % new_tool_request)
                return HttpResponseRedirect(reverse('sharing:asked-request-detail', kwargs = {'tool_request_id': new_tool_request.id}))
            else:
                return render_to_response('Sharing/asked_request_edit.html', {'form': form, 'tool_request' : tool_request, 'back' : request.META.get('HTTP_REFERER')}, context)
        else:
            form = RequestModelForm(instance=tool_request)
            return render_to_response('Sharing/asked_request_edit.html', {'form': form, 'tool_request' : tool_request, 'back' : request.META.get('HTTP_REFERER')}, context)
    else:
        messages.add_message(request,messages.ERROR, 'You are not authorised to edit this tool request')
        return HttpResponseRedirect(reverse('sharing:asked-request-detail', kwargs = {'tool_request_id':tool_request_id}))

def received_request_detail(request, tool_request_id):
    profile = UserProfile.objects.get(user = request.user)
    tool_request = Request.objects.get(id = tool_request_id )

    can_approve = tool_request.can_be_managed_by(profile)

    if request.POST:
        if can_approve:
            if 'btn_approve' in request.POST:
                tool_request.approved = True
            else:
                tool_request.approved = False
            tool_request.save()
            messages.add_message(request, messages.SUCCESS, 'Request was approved successfully')
            if tool_request.tool.is_in_shed():
                return HttpResponseRedirect(reverse('sharing:received-requests-coordinator'))
            else:
                return HttpResponseRedirect(reverse('sharing:received-requests'))
        else:
            pass
    else:
        tool_request = Request.objects.get(pk=tool_request_id)
        return render(request, 'Sharing/received_request_detail.html', {'tool_request': tool_request,'can_approve':can_approve, 'back' : request.META.get('HTTP_REFERER')})

def create_sharing(request, tool_request_id):
    context = RequestContext(request)
    tool_request = Request.objects.get(id = tool_request_id)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)

    if(tool_request.can_be_managed_by(request.user.profile)):
        if(now >= tool_request.start_date and now <= tool_request.end_date):
            if request.POST:
                form = SharingModelForm(request.POST)
                if form.is_valid():
                    new_sharing = form.save(commit=False)
                    new_sharing.pickup_arrangement = tool_request.pickup_arrangement
                    new_sharing.borrower = tool_request.borrower
                    new_sharing.lender = tool_request.lender
                    new_sharing.tool = tool_request.tool
                    new_sharing.start_date = tool_request.start_date
                    new_sharing.end_date = tool_request.end_date
                    new_sharing.save()
                    form.save_m2m()
                    tool_request.sharing = new_sharing
                    tool_request.save()
                    messages.add_message(request, messages.SUCCESS, 'Tool %s is now in possesion of %s' % (new_sharing.tool, new_sharing.borrower))
                    if tool_request.tool.is_in_shed():
                        return HttpResponseRedirect(reverse('sharing:given-tools-coordinator'))
                    else:
                        return HttpResponseRedirect(reverse('sharing:given-tools'))
                else:
                    return render_to_response('Sharing/create_sharing.html', {'form': form, 'tool_request': tool_request.tool, 'back' : request.META.get('HTTP_REFERER')}, context)
            else:
                print("GET")
                form = SharingModelForm(initial={'start_date' : tool_request.start_date, 'end_date' : tool_request.end_date})
                form.fields['start_date'].widget.attrs['readonly'] = True
                form.fields['end_date'].widget.attrs['readonly'] = True
                return render_to_response('Sharing/create_sharing.html', {'form': form, 'tool_request': tool_request, 'back' : request.META.get('HTTP_REFERER') }, context)
        else:
            messages.add_message(request,messages.ERROR, 'You cannot share a tool outside its requesting time period')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.add_message(request,messages.ERROR, 'You are not authorised  to share this tool')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class SharingModelForm(forms.ModelForm):
    class Meta:
        model = Sharing
        fields= ('start_date', 'end_date', 'comment',)

def given_tools_index(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    current = request.user.profile.current_given_tools()
    past = request.user.profile.past_given_tools()
    return render(request, 'Sharing/given_tools.html', {'current_given_tools': current, 'past_given_tools': past })

def given_tools_coordinator_index(request):
    sheds = request.user.profile.sheds
    return render(request, 'Sharing/given_tools_coordinator.html', {'sheds' : sheds})

class ReturnSharingModelForm(forms.ModelForm):
    class Meta:
        model = Sharing
        fields= ('returned', 'rated', 'sharing_comment')
    def clean(self):
        rated = self.cleaned_data.get('rated')
        if rated < 1 or rated > 5:
            raise forms.ValidationError("Rate Should be from 1 to 5")
        return self.cleaned_data


def given_tool_edit(request, tool_sharing_id):
    context = RequestContext(request)
    tool_sharing = Sharing.objects.get(id = tool_sharing_id)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    if((tool_sharing.lender == request.user.profile) and (tool_sharing.returned == False)):
        if request.POST:
            form = ReturnSharingModelForm(request.POST, request.FILES, instance=tool_sharing)
            if form.is_valid():
                new_tool_sharing = form.save()
                new_tool_sharing.finished = True
                new_tool_sharing.save()
                messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully set as returned' % new_tool_sharing)
                if tool_sharing.tool.is_in_shed():
                    return HttpResponseRedirect(reverse('sharing:given-tools-coordinator'))
                else:
                    return HttpResponseRedirect(reverse('sharing:given-tools'))
            else:
                return render_to_response('Sharing/given_tool_edit.html', {'form': form, 'tool_sharing' : tool_sharing, 'back' : request.META.get('HTTP_REFERER')}, context)
        else:
            form = ReturnSharingModelForm(instance=tool_sharing)
            return render_to_response('Sharing/given_tool_edit.html', {'form': form, 'tool_sharing' : tool_sharing, 'back' : request.META.get('HTTP_REFERER')}, context)
    else:
        messages.add_message(request,messages.ERROR, 'You are not authorised to edit this tool sharing')
        return HttpResponseRedirect(reverse('sharing:given-tools'))

def borrowed_tools_index(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    current = Sharing.objects.filter( Q(borrower=request.user.profile) & Q(returned=False) & Q(finished=False)).order_by('-start_date')
    past = Sharing.objects.filter(Q(borrower=request.user.profile) & (Q(end_date__lt=now) | Q(finished=True))).order_by('-start_date')
    return render(request, 'Sharing/borrowed_tools.html', {'current_borrowed_tools': current, 'past_borrowed_tools': past })

####++++++++++++++++++++++Community Statistics+++++++++++++++++++++++++++++ ###########
@login_required(login_url='users:login')
def statistics(request):
    Sharezone = request.user.profile.sharezone
    if request.method == 'GET':
        frequenttool = GetMostUsedTool(Sharezone)
        frequentborrower = GetFrequentBorrower(Sharezone)
        frequentlender = GetFrequentLender(Sharezone)
        toolcount = TotalTools(Sharezone)
        usercount = TotalUsers(Sharezone)
        shedcount = TotalSheds(Sharezone)
        top_borrower_rating = get_top_borrower_rating(Sharezone, 5)
        username_borrow = None
        username_lender = None
        if frequentborrower:
            username_borrow = frequentborrower.user.get_username()
        if frequentlender:
            username_lender = frequentlender.user.get_username()
        return render(request, 'Sharing/statistics.html',{'tool':frequenttool,'borrower':username_borrow,'lender':username_lender,'totaltool':toolcount,'totaluser':usercount,'totalshed':shedcount, 'top_borrower_rating': top_borrower_rating})
