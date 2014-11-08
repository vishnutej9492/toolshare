from django.conf.urls import patterns, include, url
from Sharing import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^approve/', views.mytools, name='approve'),
)