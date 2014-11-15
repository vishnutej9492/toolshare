from django.conf.urls import patterns, include, url
from Sharing import views

urlpatterns = patterns('',
    url(r'^requests/', views.mytools, name='requests'),
)
