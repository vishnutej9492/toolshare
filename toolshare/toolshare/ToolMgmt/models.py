from django.db import models
from UserAuth.models import UserProfile

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
    category = models.ForeignKey(ToolCategory)
    status = models.ForeignKey(ToolStatus)
    owner = models.ForeignKey(UserProfile, null=True)
    image = models.ImageField(upload_to="images/tools/", blank=True, null=True)
    identifier = models.CharField(verbose_name="Identifier", blank=True, null=True, max_length=200)

    def __str__(self):
        return self.name
