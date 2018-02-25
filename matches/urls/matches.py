
from django.conf.urls import url

from matches.views.matches import MatchView, ControlView, CreateMatchView, ListMatchView
app_name = "matches"

urlpatterns = [
    url(r'^create/$', CreateMatchView.as_view(), name='create'),
    url(r'^list/$', ListMatchView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', MatchView.as_view(), name='overlay'),
    url(r'^(?P<pk>\d+)/control$', ControlView.as_view(), name='control'),
]
