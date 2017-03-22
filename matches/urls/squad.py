
from django.conf.urls import url

from matches.views.squad import ImportView

urlpatterns = [
    url(r'^import/$', ImportView.as_view(), name='import'),
]
