from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView

from matches.forms import BuildMatch
from matches.models import Match
from xwing_data.models import DamageCard, DamageDeck


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
        context['faction_one'] = context['match'].squad_one.pilots.first().pilot.faction.icon()
        context['faction_two'] = context['match'].squad_two.pilots.first().pilot.faction.icon()
        return context


class ControlView(MatchView):
    template_name = 'control/control.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tfa'] = DamageCard.objects.filter(deck=DamageDeck.objects.get(name="TFA"))
        context['core'] = DamageCard.objects.exclude(deck=DamageDeck.objects.get(name="TFA"))
        return context
