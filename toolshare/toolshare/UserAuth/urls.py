from django.conf.urls import patterns,url
from UserAuth import views

urlpatterns = patterns('' ,
        # url(r'^index/$',views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$',views.user_login, name='login'),
        url(r'^$',views.user_login, name='login'),
        url(r'^edit/$',views.user_edit, name='edit'),
        url(r'^logout/$',views.user_logout, name='logout'),
        url(r'^preferences/$',views.user_preferences, name = 'preferences'), 
        url(r'^change_password/$',views.changepassword, name = 'change_password'),
        )
