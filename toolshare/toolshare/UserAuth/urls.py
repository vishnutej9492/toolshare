from django.conf.urls import patterns,url
from UserAuth import views

urlpatterns = patterns('' ,
        url(r'^$', views.LoginView.as_view(), name='login')
        )
