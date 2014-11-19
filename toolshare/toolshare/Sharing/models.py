from django.db import models

# Create your models here.

class ShareZone(models.Model):   
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    zipcode = models.IntegerField(verbose_name ="Zipcode")
    
    def __str__(self):
        return self.name

class Shed(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    sharezone = models.ForeignKey(ShareZone,related_name = 'sheds',null =True,blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Coordinator(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    user = models.ForeignKey('UserAuth.UserProfile',unique=True)
    shed = models.ForeignKey(Shed, unique = True)
    created_at = models.DateTimeField(auto_now_add = True)

class Arrangement(models.Model):
    request_date = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_arrangement = models.CharField(verbose_name="Arrangement", max_length=200)
    borrower = models.ForeignKey('UserAuth.UserProfile',related_name='borrowers')
    lender = models.ForeignKey('UserAuth.UserProfile',related_name='lenders')
    def __str__(self):
        return str(self.lender.username) +"==>" +str(self.borrower.username)

class Sharing(Arrangement): 
    def __str__(self):
        return self.name

class Request(Arrangement):
    approved = models.BooleanField()
    def __str__(self):
        return self.name
