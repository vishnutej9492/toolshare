from django.db import models

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

    def __str__(self):
        return self.name

class UserShedAssignation(models.Model):
    user_profile = models.ForeignKey('UserAuth.UserProfile', related_name='user_shed_assignations', unique=True)
    shed = models.ForeignKey(Shed, related_name='user_shed_assignations', unique = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "<" + str(self.user_profile) + "> coordinates <" + str(self.shed) + ">"

class Arrangement(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_arrangement = models.CharField(verbose_name="Arrangement", max_length=200)
    borrower = models.ForeignKey('UserAuth.UserProfile',related_name='borrowers')
    lender = models.ForeignKey('UserAuth.UserProfile',related_name='lenders')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.lender.username) + "==>" + str(self.borrower.username)

class Sharing(Arrangement): 
    comment = models.CharField(verbose_name="Arrangement", max_length=200)
    returned = models.BooleanField(default=False)

class Request(Arrangement):
    msg = models.CharField(verbose_name="Arrangement", max_length=200)
    approved = models.BooleanField(default=False)
