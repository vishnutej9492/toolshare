from django.db import models
import datetime
from django.utils.timezone import utc

class ShareZone(models.Model):   
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    zipcode = models.IntegerField(verbose_name ="Zipcode")
    
    def __str__(self):
        return self.name

class Shed(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    sharezone = models.ForeignKey(ShareZone, related_name = 'sheds',null =True,blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    coordinators = models.ManyToManyField('UserAuth.UserProfile', related_name = 'sheds', null =True,blank = True)

    def waiting_received_requests(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        waiting_requests = Request.objects.raw("SELECT Sharing_request.* FROM Sharing_request, Sharing_arrangement, ToolMgmt_tool " +
                                               "WHERE Sharing_request.arrangement_ptr_id = Sharing_arrangement .id " +
                                               "AND Sharing_arrangement.tool_id = ToolMgmt_tool.id " +
                                               "AND ToolMgmt_tool.shed_id = %s " +
                                               "AND Sharing_request.approved=0 " +
                                               "AND Sharing_request.sharing_id isnull " +
                                               "AND Sharing_arrangement.end_date >= %s " +
                                               "ORDER BY  Sharing_arrangement.start_date DESC", [self.id, now] )
        return list(waiting_requests)

    def approved_received_requests(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        approved_requests = Request.objects.raw("SELECT Sharing_request.* FROM Sharing_request, Sharing_arrangement, ToolMgmt_tool " +
                                               "WHERE Sharing_request.arrangement_ptr_id = Sharing_arrangement .id " +
                                               "AND Sharing_arrangement.tool_id = ToolMgmt_tool.id " +
                                               "AND ToolMgmt_tool.shed_id = %s " +
                                               "AND Sharing_request.approved=1 " +
                                               "AND Sharing_request.sharing_id isnull " +
                                               "AND Sharing_arrangement.end_date >= %s " +
                                               "ORDER BY  Sharing_arrangement.start_date DESC", [self.id, now] )
        return list(approved_requests)

    def past_received_requests(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        approved_requests = Request.objects.raw("SELECT Sharing_request.* FROM Sharing_request, Sharing_arrangement, ToolMgmt_tool " +
                                               "WHERE Sharing_request.arrangement_ptr_id = Sharing_arrangement .id " +
                                               "AND Sharing_arrangement.tool_id = ToolMgmt_tool.id " +
                                               "AND ToolMgmt_tool.shed_id = %s " +
                                               "AND Sharing_request.approved=1 " +
                                               "AND Sharing_request.sharing_id notnull " +
                                               "AND Sharing_arrangement.end_date < %s " +
                                               "ORDER BY  Sharing_arrangement.start_date DESC", [self.id, now] )
        return list(approved_requests)

    def current_given_tools(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        current_tools = Sharing.objects.raw("SELECT Sharing_sharing.* FROM Sharing_sharing, Sharing_arrangement, ToolMgmt_tool " +
                                               "WHERE Sharing_sharing.arrangement_ptr_id = Sharing_arrangement .id " +
                                               "AND Sharing_arrangement.tool_id = ToolMgmt_tool.id " +
                                               "AND ToolMgmt_tool.shed_id = %s " +
                                               "AND Sharing_sharing.returned=0 " +
                                               "AND Sharing_sharing.finished=0 " +
                                               "ORDER BY  Sharing_arrangement.start_date DESC", [self.id] )
        return list(current_tools)

    def past_given_tools(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        past_tools = Sharing.objects.raw("SELECT Sharing_sharing.* FROM Sharing_sharing, Sharing_arrangement, ToolMgmt_tool " +
                                               "WHERE Sharing_sharing.arrangement_ptr_id = Sharing_arrangement .id " +
                                               "AND Sharing_arrangement.tool_id = ToolMgmt_tool.id " +
                                               "AND ToolMgmt_tool.shed_id = %s " +
                                               "AND (Sharing_sharing.finished=1 OR Sharing_arrangement.end_date < %s) " +
                                               "ORDER BY  Sharing_arrangement.start_date DESC", [self.id, now] )
        return list(past_tools)

    def __str__(self):
        return self.name

class Arrangement(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_arrangement = models.CharField(verbose_name="Arrangement", max_length=200)
    borrower = models.ForeignKey('UserAuth.UserProfile',related_name='asked_requests')
    lender = models.ForeignKey('UserAuth.UserProfile',related_name='recieved_requests')
    tool = models.ForeignKey('ToolMgmt.Tool',related_name='tools', null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "borrower: <"+ str(self.borrower) + "> lender: <" + str(self.lender) + ">"

    def can_be_managed_by(self, profile):
        result = False
        if self.tool.shed == None:
            result = (profile == self.lender)
        else:
            result = (profile in self.tool.shed.coordinators.all())
        return result

class Sharing(Arrangement): 
    comment = models.CharField(verbose_name="Comment about the sharing", max_length=200)
    returned = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    rated = models.PositiveSmallIntegerField(default=1)
    sharing_comment = models.CharField(verbose_name="Comment about on how the sharing", max_length=200, null =True, blank = True)

    def __str__(self):
        if(self.tool.shed_id == None):
            lender = self.lender
        else:
            lender = Shed.objects.filter(id=self.tool.shed_id).first()

        return "<"+ str(self.borrower) + "> has <" + str(self.tool) + "> from <" + str(lender) + ">"

class Request(Arrangement):
    msg = models.CharField(verbose_name="Arrangement message for requesting", max_length=200)
    approved = models.BooleanField(default=False)
    sharing = models.OneToOneField(Sharing, related_name='request', null =True, blank = True)

    def __str__(self):
        if(self.tool.shed_id == None):
            lender = self.lender
        else:
            lender = Shed.objects.filter(id=self.tool.shed_id).first()

        return "<"+ str(self.borrower) + "> has requested <" + str(lender) + "> a <" + str(self.tool) + ">"
