from django.db.models import Model, CharField, IntegerField, DateTimeField, BooleanField
from rest_framework import serializers



class Match(Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    nick_name = CharField(max_length=64, null=True)
    turn_of = IntegerField(null=True)
    ended = BooleanField(null=True)


    class Meta:
        db_table = '"game"."match"'
        managed = True

    def __str__(self):
        return self.nick_name



class MatchSerializer(serializers.Serializer):
    model = Match
    fields = '__all__'