import codecs

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
import json

from matches.forms import ImportForm
from matches.models import Squad
from matches.tasks import import_squad


class ImportView(FormView):
    template_name = 'import.html'
    form_class = ImportForm

    success_url = reverse_lazy("home")

    def form_valid(self, form):
        xws_file = form.cleaned_data['xws_file']
        reader = codecs.getreader("utf-8")
        data = json.load(reader(xws_file))
        squad = Squad.objects.get(pk=import_squad(data, form.cleaned_data['player_name']))
        messages.success(self.request, "{} successfully imported".format(squad.list_name))
        return super().form_valid(form)
