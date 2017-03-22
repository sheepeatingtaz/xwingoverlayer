
from django.conf.urls import url

from matches.views import MatchView

urlpatterns = [
    url(r'^(?P<pk>\d+)/', MatchView.as_view(), name='overlay'),
]
