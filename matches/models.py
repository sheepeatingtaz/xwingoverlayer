import datetime

from django.db import models
from django.urls import reverse
from django.urls import reverse_lazy

from xwing_data.models import Pilot, Upgrade, StatisticSet
from django.utils import timezone


class MatchUpgrade(models.Model):
    def __str__(self):
        description = self.upgrade.__str__()
        # if not self.active:
        #     description += " (removed)"
        return description

    upgrade = models.ForeignKey(Upgrade)
    active = models.BooleanField(default=True)


class MatchPilot(models.Model):
    def __str__(self):
        return "{} ({})".format(
            self.pilot.name,
            self.pilot.ship.name
        )

    def upgrade_list(self):
        upgrades = []
        for upgrade in self.upgrades.all():
            upgrades.append(
                "<span{}>{}</span>".format(
                    "" if upgrade.active else " class='disabled'",
                    upgrade.upgrade.name
                )
            )
        return " &bull; ".join(upgrades)

    pilot = models.ForeignKey(Pilot)
    points = models.IntegerField(default=0)

    upgrades = models.ManyToManyField(MatchUpgrade, blank=True)
    stats = models.ForeignKey(StatisticSet)


class Squad(models.Model):
    def __str__(self):
        return "{} ({})".format(
            self.list_name,
            self.player_name
        )

    player_name = models.CharField(max_length=200, default="Joe Bloggs")
    list_name = models.CharField(max_length=200, default="Unnamed List")
    pilots = models.ManyToManyField(MatchPilot)


class Match(models.Model):
    def __str__(self):
        return "{} vs {}".format(
            self.squad_one,
            self.squad_two
        )

    def end_time(self):
        if self.start_time and self.match_minutes:
            ts = self.start_time + datetime.timedelta(minutes=self.match_minutes)
        else:
            ts = timezone.now() + datetime.timedelta(minutes=self.match_minutes)
        return ts

    def get_absolute_url(self):
        return reverse_lazy('matches:control', kwargs={'pk': self.id})

    def get_overlay_url(self):
        return reverse_lazy('matches:overlay', kwargs={'pk': self.id})

    squad_one = models.ForeignKey(Squad, related_name="list_one")
    squad_two = models.ForeignKey(Squad, related_name="list_two")
    start_time = models.DateTimeField(blank=True, null=True)
    match_minutes = models.IntegerField(default=75)
