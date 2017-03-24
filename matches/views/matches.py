from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView

from matches.forms import BuildMatch
from matches.models import Match

FACTION_MAP = {
    "Galactic Empire": "empire",
    "First Order": "firstorder",
    "Rebel Alliance": "rebel",
    "Resistance": "rebel",
    "Scum and Villainy": "scum",

}

class CreateMatchView(CreateView):
    template_name = 'create_match.html'
    form_class = BuildMatch

    def post(self, request, *args, **kwargs):
        if "save" in request.POST:
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))


class ListMatchView(ListView):
    template_name = "list.html"
    model = Match
    context_object_name = "matches"


class MatchView(TemplateView):
    template_name = 'basic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = get_object_or_404(Match, pk=kwargs.get('pk'))
        context['faction_one'] = FACTION_MAP[context['match'].squad_one.pilots.first().pilot.faction.name]
        context['faction_two'] = FACTION_MAP[context['match'].squad_two.pilots.first().pilot.faction.name]
        return context


class ControlView(MatchView):
    template_name = 'control/control.html'
