from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toolshare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^home/', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('UserAuth.urls',namespace="users")),
    url(r'^toolmgmt/', include('ToolMgmt.urls', namespace="toolmgmt")),
)
