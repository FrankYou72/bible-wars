from django.db.models import Model, CharField
from rest_framework import serializers


class CardType(Model):
    name = CharField(max_length=128, null=True)
    identifier = CharField(max_length=16, primary_key=True)

    class Meta:
        db_table = '"game"."card_type"'
        managed = True

    def __str__(self):
        return self.name

class CardTypeSerializer(serializers.Serializer):
    model = CardType
    fields = '__all__'