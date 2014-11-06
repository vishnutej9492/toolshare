from django.conf.urls import patterns, include, url
from ToolMgmt import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='tools/', permanent=False), name='tools'),
    url(r'^tools/$', views.index, name='tools'),
    url(r'^tools/mytools/', views.mytools, name='mytools'),
    url(r'^tools/register/$', views.register, name="register"),
    url(r'^(?P<tool_id>\d+)/$', views.detail, name='detail'),
)
