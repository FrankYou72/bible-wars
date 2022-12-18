from django.db import transaction
from math import ceil, floor

from ..models.cell import Cell
from ..models.item import Item
from .arena import are_linear, distance
from ...utils.exceptions import OccupiedCellError, NotLinearCells, EnemyTooFar
from ...utils.dice import d50


@transaction.atomic
def move(player, cell):
    if not cell.is_vacant():
        raise OccupiedCellError

    current_cell = Cell.objects.get(player=player)
    current_cell.player = None
    current_cell.save()

    cell.player = player
    cell.save()


def attack(player1, player2, weapon=None, shield=None):
    cell1 = Cell.objects.get(player=player1)
    cell2 = Cell.objects.get(player=player2)

    if not are_linear(cell1, cell2):
        raise NotLinearCells

    _range = weapon.range if weapon else 1

    if distance(cell1, cell2) > _range:
        raise EnemyTooFar


    if weapon:
        weapon.consequence.apply(player1)
    if shield:
        shield.consequence.apply(player2)

    player_attack = player1.attack_power()
    player_defense = player2.defense_power()

    die_attack = d50()
    die_defense = d50()

    if die_attack == 50:
        die_attack += 5

    if die_defense == 50:
        die_defense += 5

    total_attack = player_attack + die_attack
    total_defense = player_defense + die_defense

    balance = total_attack - total_defense
    hit_points = ceil(balance / 5)

    if balance > 0:
        winner = player1
        hp_loss = floor(balance/10)

    else:
        winner = player2
        hp_loss = 0

    player1.score += hit_points
    player2.hp -= hp_loss

    if weapon:
        weapon.consequence.unnapply(player1)
    if shield:
        shield.consequence.unnapply(player2)

    player1.save()
    player2.save()

    return {
        "attacker" : player1,
        "defender" : player2,
        "total_attack" : total_attack,
        "total_defense": total_defense,
        "balance": balance,
        "winner" : winner
    }











