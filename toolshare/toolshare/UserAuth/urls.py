from django.conf.urls import patterns,url,include 
from django.views.generic import TemplateView
from UserAuth import views

urlpatterns = patterns('' ,
        (r'^$',TemplateView.as_view(template_name="UserAuth/signin.html"))
         #url(r'^$', views.login,name='login'),
         
         )
