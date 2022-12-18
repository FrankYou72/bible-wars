from django.db.models import Model, ForeignKey, PROTECT
from rest_framework import serializers

from .character import Character, CharacterSerializer
from .event import Event, EventSerializer


class SpecialMove(Model):
    event = ForeignKey(Event, null=True, on_delete=PROTECT)
    character = ForeignKey(Character, null=True, on_delete=PROTECT)


    class Meta:
        db_table = '"game"."special_move"'
        managed = True

    def __str__(self):
        return f'{self.character}: {self.event}'



class SpecialMoveSerializer(serializers.Serializer):
    model = SpecialMove
    character = CharacterSerializer()
    event = EventSerializer()
    fields = '__all__'