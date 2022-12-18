from django.db import transaction

from ..models.player import Player
from ..models.bag import Bag
from ..models.body import Body


@transaction.atomic
def new_player(user, character, lives=2):
    player = Player()
    player.user = user
    player.character = character
    player.level = 1
    player.score = 0
    player.lives = 2
    player.is_alive = True

    bag = Bag()
    bag.save()

    body = Body()
    body.save()

    player.bag = bag
    player.body = body
    player.save()

    return player
