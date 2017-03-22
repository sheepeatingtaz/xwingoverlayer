
from django.conf.urls import url

from matches.views import MatchView, ControlView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', MatchView.as_view(), name='overlay'),
    url(r'^(?P<pk>\d+)/control$', ControlView.as_view(), name='control'),
]
