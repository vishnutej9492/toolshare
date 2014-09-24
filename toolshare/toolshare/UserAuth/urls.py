from django.conf.urls import patterns,url,include 

from UserAuth import views

urlpatterns = patterns('' ,
         url(r'^$', views.login, name='login')
         )
