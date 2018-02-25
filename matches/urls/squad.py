
from django.conf.urls import url

from matches.views.squad import ImportView

app_name="squad"
urlpatterns = [
    url(r'^import/$', ImportView.as_view(), name='import'),
]
