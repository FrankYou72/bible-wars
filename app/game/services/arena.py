from django.db import transaction
from math import sqrt

from ..models.arena import Arena
from ..models.cell import Cell
from ...utils.alphabet import alphabet


@transaction.atomic
def new_arena(rows, columns, match):
    arena = Arena()
    arena.rows = rows
    arena.columns = columns
    arena.match = match
    arena.save()

    letters = alphabet[:columns]

    for letter in letter:
        for i in range(1, rows+1):
            cell = Cell()
            cell.row = i
            cell.column = letter
            cell.arena = arena
            cell.save()

    return arena



def distance(cell1, cell2):
    row1 = cell1.row
    row2 = cell2.row

    index1 = alphabet.index(cell1.column)
    index2 = alphabet.index(cell2.column)

    distance = sqrt((index2-index1)**2 + (row2 - row1)**2)

    return distance


def are_linear(cell1, cell2):
    if cell1.row == cell2.row:
        return True
    if cell1.column == cell2.column:
        return True

    index1 = alphabet.index(cell1.column)
    index2 = alphabet.index(cell2.column)

    if abs(index2 - index1) == abs(cell2.row - cell1.row):
        return True

    return False
