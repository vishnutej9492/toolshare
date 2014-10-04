from django.db import models

class ToolCategory(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)

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

    def __str__(self):
        return self.name