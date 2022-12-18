from random import choice
from django.db import transaction

from ..models.match import Match
from ..models.player import Player
from ...utils.exceptions import TooLittlePlayers


@transaction.atomic
def new_match(nick_name, players):
    if len(players) < 2:
        raise TooLittlePlayers

    next = choice(players)

    match = Match()
    match.nick_name = nick_name
    match.ended = False
    match.turn_of = next
    match.save()

    for player_id in players:
        player = Player.objects.get(id=player_id)
        player.match = match
        player.save()

    return match
