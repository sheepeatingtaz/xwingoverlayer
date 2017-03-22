from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from matches.models import Match


class MatchView(TemplateView):
    template_name = 'basic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = get_object_or_404(Match, pk=kwargs.get('pk'))
        return context


class ControlView(MatchView):
    template_name = 'control/control.html'
