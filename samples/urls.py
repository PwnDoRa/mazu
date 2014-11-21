#! -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.conf.urls import url

from views import SampleUploadView
from views import SampleUpdateView
from views import MalwareDeleteView
from views import MalwareProfileView
from views import MalwarePublishView
from views import SampleListView
from views import SourceUpdateView
from views import SourceDeleteView
from views import SourceListView
from views import SourceCreateView
from views import download


urlpatterns = patterns(
    '',
    url(r'^source/create/$', SourceCreateView.as_view(), name='source.create'),
    url(r'^source/list/$', SourceListView.as_view(), name='source.list'),
    url(r'^source/update/(?P<slug>[\w]+)/$', SourceUpdateView.as_view(), name='source.update'),
    url(r'^source/delete/(?P<slug>[\w]+)/$', SourceDeleteView.as_view(), name='source.delete'),
    url(r'^upload/$', SampleUploadView.as_view(), name='malware.upload'),
    url(r'^download/(?P<slug>[\w]+)/$', download, name='malware.download'),
    url(r'^list/$', SampleListView.as_view(), name='malware.list'),
    url(r'^list/(?P<slug>[\w]+)/$', SampleListView.as_view(), name='malware.source.filter'),
    url(r'^profile/(?P<slug>[\w]+)/$', MalwareProfileView.as_view(), name='malware.profile'),
    url(r'^delete/(?P<slug>[\w]+)/$', MalwareDeleteView.as_view(), name='malware.delete'),
    url(r'^update/(?P<slug>[\w]+)/$', SampleUpdateView.as_view(), name='malware.update'),
    url(r'^publish/(?P<slug>[\w]*)/$', MalwarePublishView.as_view(), name='malware.publish'),
)
