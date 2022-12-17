from django.db.models import Model, ForeignKey, IntegerField, BooleanField, PROTECT
from django.contrib.auth.models import User
from rest_framework import serializers

from .character import Character, CharacterSerializer
from .match import Match, MatchSerializer
from .bag import Bag, BagSerializer
from .body import Body, BodySerializer


class Player(Model):
    character = ForeignKey(Character, null=True, on_delete=PROTECT)
    match = ForeignKey(Match, null=True, on_delete=PROTECT)
    level = IntegerField(null=True)
    score = IntegerField(null=True)
    lives = IntegerField(null=True)
    is_alive = BooleanField(null=True)
    user = ForeignKey(User, null=True, on_delete=PROTECT)
    bag = ForeignKey(Bag, null=True, on_delete=PROTECT)
    body = ForeignKey(Body, null=True, on_delete=PROTECT)


    class Meta:
        db_table = '"game"."player"'
        managed = True

    def __str__(self):
        return self.user



class PlayerSerializer(serializers.Serializer):
    model = Player
    character = CharacterSerializer()
    match = MatchSerializer()
    body = BodySerializer()
    fields = '__all__'