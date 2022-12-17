from django.db.models import Model, CharField, ForeignKey, PROTECT
from rest_framework import serializers

from .consequence import Consequence, ConsequenceSerializer


class Origin(Model):
    name = CharField(max_length=32, null=True)
    consequence = ForeignKey(Consequence, null=True, on_delete=PROTECT)


    class Meta:
        db_table = '"game"."origin"'
        managed = True

    def __str__(self):
        return self.name



class OriginSerializer(serializers.Serializer):
    model = Origin
    consequence = ConsequenceSerializer()
    fields = '__all__'