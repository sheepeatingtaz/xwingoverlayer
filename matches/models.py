from django.db import models

from xwing_data.models import Pilot, Upgrade, StatisticSet


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
        return " &bull; ".join(self.upgrades.values_list('upgrade__name', flat=True))

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

    squad_one = models.ForeignKey(Squad, related_name="list_one")
    squad_two = models.ForeignKey(Squad, related_name="list_two")
    start_time = models.DateTimeField()
    match_minutes = models.IntegerField(default=75)
