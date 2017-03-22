from celery import shared_task
from django.contrib.contenttypes.models import ContentType

from matches.models import Squad, MatchPilot, MatchUpgrade, Match
from xwing_data.models import Pilot, Upgrade, StatisticSet


@shared_task(bind=True, max_retries=3)
def delete_all_data(self):
    Squad.objects.all().delete()
    MatchPilot.objects.all().delete()
    MatchUpgrade.objects.all().delete()
    Match.objects.all().delete


@shared_task(bind=True, max_retries=3)
def import_squad(self, xws, player_name):
    squad = Squad(
        player_name=player_name,
        list_name=xws.get("name")
    )

    squad.save()

    for pilot in xws.get("pilots", []):
        pilot_data = Pilot.objects.get(xws=pilot.get("name"))
        if pilot_data.ship_override:
            target = pilot_data.ship_override
        else:
            target = pilot_data.ship.stats

        target.skill = pilot_data.skill

        stats = StatisticSet(
            skill=target.skill,
            attack=target.attack,
            agility=target.agility,
            hull=target.hull,
            shields=target.shields
        )

        stats.save()

        match_pilot = MatchPilot(
            pilot=pilot_data,
            points=pilot.get("points"),
            stats=stats,
        )
        match_pilot.save()
        if pilot.get('upgrades', []):
            for upgrade_type, upgrades in pilot['upgrades'].items():
                for upgrade in upgrades:
                    upgrade_object = Upgrade.objects.get(xws=upgrade)
                    match_upgrade = MatchUpgrade(upgrade=upgrade_object)
                    match_upgrade.save()
                    match_pilot.upgrades.add(match_upgrade)
                    for grant in upgrade_object.grants.all():
                        if grant.content_type == ContentType.objects.get(model="statisticset"):
                            for field in ["skill", "attack", "agility", "hull", "shields"]:
                                setattr(
                                    match_pilot.stats,
                                    field,
                                    getattr(grant.content_object, field, 0) + getattr(match_pilot.stats, field, 0)
                                )
                            match_pilot.stats.save()

        squad.pilots.add(match_pilot)

    return squad.id

    # TODO, add extra fields, like link etc?
