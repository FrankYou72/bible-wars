from django.db.models import Model, CharField, IntegerField, TextField, BooleanField
from rest_framework import serializers


class Character(Model):
    name = CharField(max_length=128, null=True)
    info = TextField(null=True)
    hp = IntegerField(null=True)
    power = IntegerField(null=True)
    wisdom = IntegerField(null=True)
    faith = IntegerField(null=True)
    attack = IntegerField(null=True)
    defense = IntegerField(null=True)
    speed = IntegerField(null=True)
    alliance = CharField(max_length=64, null=True)
    is_minion = BooleanField(null=True)
    playable = BooleanField(null=True)

    class Meta:
        db_table = '"game"."character"'
        managed = True

    def __str__(self):
        return self.name



class CharacterSerializer(serializers.Serializer):
    model = Character
    fields = '__all__'