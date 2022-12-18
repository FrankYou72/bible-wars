from django.db.models import Model, IntegerField, ForeignKey, PROTECT
from rest_framework import serializers

from .match import Match


class Arena(Model):
    rows = IntegerField(null=True)
    columns = IntegerField(null=True)
    match = ForeignKey(Match, on_delete=PROTECT, null=True)

    class Meta:
        db_table = '"game"."arena"'
        managed = True

    def __str__(self):
        return f'{self.rows}x{self.columns}'



class ArenaSerializer(serializers.Serializer):
    model = Arena
    fields = '__all__'