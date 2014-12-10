from django.db import models
from UserAuth.models import UserProfile
from Sharing.models import ShareZone, Shed, Sharing, Request
from django.db.models import Q
import datetime
from django.utils.timezone import utc

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
