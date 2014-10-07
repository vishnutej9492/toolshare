from django.conf.urls import patterns,url
from UserAuth import views

urlpatterns = patterns('' ,
        url(r'^index/$',views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$',views.user_login, name='login'),
        url(r'^$',views.user_login, name='login'),
        url(r'^edit1/$',views.user_edit1, name='edit1'),
        url(r'^logout/$',views.user_logout, name='logout'),
        )
