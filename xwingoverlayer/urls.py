from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from matches.views.home import HomeView, DeleteDataView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^clear/$', DeleteDataView.as_view(), name='delete'),
    url(r'^match/', include('matches.urls.matches')),
    url(r'^squad/', include('matches.urls.squad')),
]
