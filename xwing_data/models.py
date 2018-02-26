import re
from collections import OrderedDict

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.models import TimeStampedModel


class Base(TimeStampedModel):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)


class XWSBase(Base):
    class Meta:
        abstract = True

    id = models.IntegerField(unique=True, primary_key=True)
    xws = models.CharField(max_length=100)


class Faction(Base):
    XWS_MAP = {
        "Galactic Empire": "imperial",
        "First Order": "imperial",
        "Rebel Alliance": "rebel",
        "Resistance": "rebel",
        "Scum and Villainy": "scum",
    }

    xws = models.CharField(max_length=100)

    def icon(self):
        FACTION_MAP = {
            "Galactic Empire": "empire",
            "First Order": "firstorder",
            "Rebel Alliance": "rebel",
            "Resistance": "rebel",
            "Scum and Villainy": "scum",

        }
        return FACTION_MAP[self.name]

    def pilot_icon(self):
        FACTION_MAP = {
            "Galactic Empire": "helmet-imperial",
            "First Order": "helmet-imperial",
            "Rebel Alliance": "helmet-rebel",
            "Resistance": "helmet-rebel",
            "Scum and Villainy": "helmet-scum",

        }
        return FACTION_MAP[self.name]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.xws = self.XWS_MAP[self.name]
        super().save(force_insert, force_update, using, update_fields)


class Action(Base):
    pass


class BaseSize(Base):
    pass


class SlotType(Base):
    pass


class StatisticSet(models.Model):
    def __str__(self):
        return "{}/{}/{}/{}/{}".format(
            self.skill,
            self.attack,
            self.agility,
            self.hull,
            self.shields
        )

    def skill_dict(self):
        d = OrderedDict()
        d["skill"] = self.skill
        d["attack"] = self.attack
        d["agility"] = self.agility
        d["hull"] = self.hull
        d["shield"] = self.shields

        return d

    skill = models.IntegerField(default=0)
    attack = models.IntegerField()
    agility = models.IntegerField()
    hull = models.IntegerField()
    shields = models.IntegerField()


class Ship(XWSBase):
    faction = models.ManyToManyField(Faction)
    stats = models.OneToOneField(StatisticSet)
    actions = models.ManyToManyField(Action)
    size = models.ForeignKey(BaseSize)


class Pilot(XWSBase):
    class Meta:
        unique_together = ('xws', 'faction', 'ship')

    is_unique = models.BooleanField(default=False)
    ship = models.ForeignKey(Ship)
    points = models.IntegerField()
    skill = models.IntegerField()
    ability = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, null=True)
    faction = models.ForeignKey(Faction)
    ship_override = models.ForeignKey(StatisticSet, blank=True, null=True)


class Slot(models.Model):
    def __str__(self):
        return self.slot_type.__str__()

    slot_type = models.ForeignKey(SlotType)
    pilot = models.ForeignKey(Pilot)


class GrantType(Base):
    pass


class Grant(Base):
    limit = models.Q(app_label='xwing_data', model='Action') | \
            models.Q(app_label='xwing_data', model='SlotType') | \
            models.Q(app_label='xwing_data', model='StatisticsSet')
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Upgrade(XWSBase):
    def __str__(self):
        return re.sub("\([+\-]\d\)", "", self.name).strip()  # Just for adaptability at the moment, get rid of the +/-1

    def static_image_url(self):
        return self.image.url.replace('')

    is_unique = models.BooleanField(default=False)
    is_limited = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)
    slot = models.ForeignKey(SlotType)
    image = models.CharField(max_length=300, blank=True, null=True)
    points = models.IntegerField()
    energy = models.IntegerField(default=0)
    faction = models.ManyToManyField(Faction, blank=True)
    range = models.CharField(max_length=5, blank=True, null=True)
    attack = models.IntegerField(default=0)
    ships = models.ManyToManyField(Ship, blank=True)
    size = models.ManyToManyField(BaseSize, blank=True)
    grants = models.ManyToManyField(Grant, blank=True)


class DamageDeck(Base):
    pass


class DamageType(Base):
    pass


class DamageCard(Base):
    amount = models.IntegerField(default=0)
    type = models.ForeignKey(DamageType)
    deck = models.ForeignKey(DamageDeck)
    text = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, null=True)
