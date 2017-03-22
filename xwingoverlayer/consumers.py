import json

from channels import Group
from channels.sessions import channel_session
from matches.models import Match


@channel_session
def ws_connect(message):
    prefix, match_id, suffix = message['path'].strip('/').split('/')
    match = Match.objects.get(pk=match_id)
    # print(prefix, match_id, match)
    Group('match-{}'.format(match_id)).add(message.reply_channel)
    # print("Group Added")
    message.channel_session['match'] = '{}'.format(match_id)
    # print("Session Set")


@channel_session
def ws_receive(message):
    match_id = message.channel_session['match']
    match = Match.objects.get(pk=match_id)
    data = json.loads(message['text'])
    m = match.messages.create(handle=data['handle'], message=data['message'])
    Group('match-{}'.format(match_id)).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    match_id = message.channel_session['match']
    Group('match-{}'.format(match_id)).discard(message.reply_channel)
