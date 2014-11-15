from django.db import models
from UserAuth.models import UserProfile
from ToolMgmt.models import Tool

# Create your models here.

class ShareZone(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    users = models.ForeignKey(UserProfile, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Shed(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    sharezone = models.ForeignKey(ShareZone)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class arrangement(models.Model):
    date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_arrangement = models.CharField(verbose_name="Arrangement", max_length=200)

    def __str__(self):
        return self.name

class sharing(models.Model):

    def __str__(self):
        return self.name

class request(models.Model):
    approved = models.BooleanField()
    def __str__(self):
        return self.name