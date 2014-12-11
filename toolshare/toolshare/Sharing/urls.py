from django.conf.urls import patterns, include, url
from Sharing import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
    #+++++++++++++++ URLS related to the SHED over here+++++++++++++++++++ #
    url(r'^sheds/$', views.sheds, name='sheds'),
    url(r'^sheds/create/$', views.shedcreate, name='shedcreate'),
    url(r'^sheds/(?P<shed_id>\d+)/$',views.sheddetail, name='sheddetail'),
    url(r'^sheds/(?P<shed_id>\d+)/edit/$', views.shededit, name='shededit'),
    url(r'sheds/(?P<shed_id>\d+)/coords/$', views.shedcoords, name='shedcoords'),
    url(r'sheds/(?P<shed_id>\d+)/coords/add/$',views.shedaddcoords,name='shedaddcoords'),
    url(r'sheds/tooltransfer/(?P<tool_id>\d+)/$',views.tooltransfer,name = 'tooltransfer'),
    url(r'sheds/returntool/(?P<tool_id>\d+)/$',views.returntool,name = 'returntool'),
    #+++++++++++++++++SHED url ends here ++++++++++++++++++++++++++++++++++#
    url(r'^$', RedirectView.as_view(url='received-requests/', permanent=False), name='received-requests'),
    url(r'^create-request/(?P<tool_id>\d+)/$', views.create_request, name='create-request'),
    url(r'^create-sharing/(?P<tool_request_id>\d+)/$', views.create_sharing, name='create-sharing'),
    url(r'^received-requests/$', views.received_requests_index, name='received-requests'),
    url(r'^received-requests-coordinator/$', views.received_requests_coordinator_index, name='received-requests-coordinator'),
    url(r'^asked-requests/$', views.asked_requests_index, name='asked-requests'),
    url(r'^received-requests/(?P<tool_request_id>\d+)/$', views.received_request_detail, name='received-request-detail'),
    url(r'^asked-requests/(?P<tool_request_id>\d+)/$', views.asked_request_detail, name='asked-request-detail'),
    url(r'^asked-requests/(?P<tool_request_id>\d+)/edit$', views.asked_request_edit, name='asked-request-edit'),
    url(r'^given-tools/$', views.given_tools_index, name='given-tools'),
    url(r'^given-tools-coordinator/$', views.given_tools_coordinator_index, name='given-tools-coordinator'),
    url(r'^given-tools/(?P<tool_sharing_id>\d+)/$', views.given_tool_edit, name='given-tool-edit'),
    url(r'^borrowed-tools/$', views.borrowed_tools_index, name='borrowed-tools'),
    #++++++++++++++++++++Statistics ++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    url(r'^statistics/$',views.statistics,name = "statistics"),
    #+++++++++++++++++++Search Tool Functionality ++++++++++++++++++++++++++#
    url(r'^searchtools/$', views.searchtools , name = 'searchtools'),
)
