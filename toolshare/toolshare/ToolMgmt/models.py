from django.db import models
from UserAuth.models import UserProfile
from Sharing.models import ShareZone, Shed, Sharing, Request
from django.db.models import Q
from datetime import date, timedelta, datetime
from django.utils.timezone import utc
from Sharing.models import ShareZone, Shed

class ToolCategory(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)

    def __str__(self):
        return self.name

class ToolStatus(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)
    description = models.CharField(verbose_name="Description", max_length=200)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(ToolCategory, related_name='category')
    status = models.ForeignKey(ToolStatus, related_name='status')
    owner = models.ForeignKey(UserProfile, related_name='owner', null=True)
    image = models.ImageField(upload_to="images/tools/", blank=True, null=True)
    identifier = models.CharField(verbose_name="Identifier", blank=True, null=True, max_length=200)
    shed = models.ForeignKey(Shed, related_name='tools', null = True, blank = True)
    in_shed = models.BooleanField(default = False)
    blackout_start_date = models.DateTimeField()
    blackout_end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def is_in_shed(self):
        return self.shed!=None

    def is_available(self, from_date, to_date):
        result = False
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        tools = Request.objects.filter(Q(tool=self) & Q(approved=True) & Q(start_date__gte=now) &
                                      ((Q(start_date__lte=from_date)&Q(end_date__gte=from_date)) |
                                      (Q(start_date__lte=to_date)&Q(end_date__gte=to_date))))
        return (tools.count() == 0)

    def date_range(self, start, end):
        d1 = datetime.strptime(start, '%Y/%m/%d')
        d2 = datetime.strptime(end, '%Y/%m/%d')
        l = []
        for i in range((d2-d1).days + 1):
            l.append( str( (d1+ timedelta(days=i)).date().strftime('%Y/%m/%d') ))
        return l

    def blackout_dates(self):
        return self.date_range('2014/12/08','2014/12/19')
