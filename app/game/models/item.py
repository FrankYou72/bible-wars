from django.db.models import Model, CharField, IntegerField, TextField, ForeignKey, PROTECT
from rest_framework import serializers

from .consequence import Consequence, ConsequenceSerializer


class Item(Model):
    name = CharField(max_length=32, null=True)
    description = TextField(null=True)
    type = CharField(max_length=64, null=True)
    range = IntegerField(null=True)
    rarity = CharField(max_length=1, null=True)
    consequence = ForeignKey(Consequence, null=True, on_delete=PROTECT)
    span = IntegerField(null=True)



    class Meta:
        db_table = '"game"."item"'
        managed = True

    def __str__(self):
        return self.name



class ItemSerializer(serializers.Serializer):
    model = Item
    consequence = ConsequenceSerializer()
    fields = '__all__'