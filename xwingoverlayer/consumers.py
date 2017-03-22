import json

from channels import Group
from channels.sessions import channel_session

from matches.models import MatchUpgrade, MatchPilot


@channel_session
def ws_connect(message):
    prefix, match_id = message['path'].strip('/').split('/')
    Group('match-{}'.format(match_id)).add(message.reply_channel)
    message.channel_session['match'] = '{}'.format(match_id)
    Group('match-{}'.format(match_id)).send({"accept": True})


@channel_session
def ws_receive(message):
    match_id = message.channel_session['match']
    data = json.loads(message['text'])

    if data.get("type") == "upgrade":
        upgrade = MatchUpgrade.objects.get(pk=data.get('id'))
        upgrade.active = bool(data.get('value'))
        upgrade.save()
        # data['upgrades'] =

    if data.get("type") == "stat":
        pilot = MatchPilot.objects.get(pk=data.get('id'))
        setattr(pilot.stats, data.get('field'), data.get('value'))
        pilot.stats.save()

    Group('match-{}'.format(match_id)).send({'text': json.dumps(data)})


@channel_session
def ws_disconnect(message):
    match_id = message.channel_session['match']
    Group('match-{}'.format(match_id)).discard(message.reply_channel)
