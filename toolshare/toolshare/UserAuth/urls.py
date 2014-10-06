from django.conf.urls import patterns,url
from UserAuth import views

urlpatterns = patterns('' ,
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$',views.user_login, name='login'),
        url(r'^edit1/$',views.user_edit1, name='edit1')
        )
