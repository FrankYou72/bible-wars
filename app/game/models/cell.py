from django.db.models import Model, CharField, IntegerField, ForeignKey, PROTECT
from rest_framework import serializers

from .player import Player, PlayerSerializer
from .item import Item, ItemSerializer
from .arena import Arena, ArenaSerializer


class Cell(Model):
    arena = ForeignKey(Arena, on_delete=PROTECT, null=True)
    row = IntegerField(null=True)
    column = CharField(max_length=1, null=True)
    player = ForeignKey(Player, on_delete=PROTECT, null=True)
    item = ForeignKey(Item, on_delete=PROTECT, null=True)
    surface_type = CharField(max_length=32, null=True)

    class Meta:
        db_table = '"game"."cell"'
        managed = True

    def __str__(self):
        return f'{self.column}{self.row}'



class CellSerializer(serializers.Serializer):
    model = Cell
    player = PlayerSerializer()
    item = ItemSerializer()
    fields = '__all__'