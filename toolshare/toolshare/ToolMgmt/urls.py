from django.conf.urls import patterns, include, url
from ToolMgmt import views
# from ToolMgmt.models import Tool

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^mytools/', views.mytools, name='mytools'),
    url(r'^register/$', views.register, name="register"),
    url(r'^(?P<tool_id>\d+)/$', views.detail, name='detail'),
)
