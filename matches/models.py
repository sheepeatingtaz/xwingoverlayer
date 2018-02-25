import datetime

from django.db import models
from django.urls import reverse
from django.urls import reverse_lazy

from xwing_data.models import Pilot, Upgrade, StatisticSet
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import escape


class MatchUpgrade(models.Model):
    def __str__(self):
        description = self.upgrade.__str__()
        # if not self.active:
        #     description += " (removed)"
        return description

    upgrade = models.ForeignKey(Upgrade, on_delete=models.CASCADE)
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

    def upgrade_list_images(self):
        upgrades = []
        for upgrade in self.upgrades.all():
            upgrades.append(
                '<img src="{}"/>'.format(
                    static('xwing-data/images/{}'.format(
                        upgrade.upgrade.image.replace(" ", "%20")
                    ))
                )
            )
        return "".join(upgrades)

    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    upgrades = models.ManyToManyField(MatchUpgrade, blank=True)
    stats = models.ForeignKey(StatisticSet, on_delete=models.CASCADE)


class Squad(models.Model):
    def __str__(self):
        return "{} ({})".format(
            self.list_name,
            self.player_name
        )

    def all_images(self):
        images = []
        for pilot in self.pilots.all():
            images.append('<img src="{}"/>'.format(
                    static('xwing-data/images/{}'.format(
                        pilot.pilot.image.replace(" ", "%20")
                    ))
                )
            )
            images.append(pilot.upgrade_list_images())
        return "".join(images)

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
            ts = timezone.now()  # + datetime.timedelta(minutes=self.match_minutes)
        return ts

    def get_absolute_url(self):
        return reverse_lazy('matches:control', kwargs={'pk': self.id})

    def get_overlay_url(self):
        return reverse_lazy('matches:overlay', kwargs={'pk': self.id})

    squad_one = models.ForeignKey(Squad, related_name="list_one", on_delete=models.CASCADE)
    squad_two = models.ForeignKey(Squad, related_name="list_two", on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    match_minutes = models.IntegerField(default=75)
