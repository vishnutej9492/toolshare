from django.conf.urls import patterns, include, url
from ToolMgmt import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.RegisterTool.as_view(), name='register'),
    url(r'^(?P<tool_id>\d+)/$', views.detail, name='detail'),
)
