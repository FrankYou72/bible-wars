from django.db.models import Model, CharField, IntegerField, ForeignKey, PROTECT
from rest_framework import serializers

from .character_class import CharacterClass, CharacterClassSerializer


class Requirement(Model):
    alliance = CharField(max_length=64, null=True)
    character_class = ForeignKey(CharacterClass, null=True, on_delete=PROTECT)
    attribute = CharField(max_length=64, null=True)
    required = IntegerField(null=True)


    class Meta:
        db_table = '"game"."requirement"'
        managed = True

    def __str__(self):
        return f'{self.attribute}: {self.required}'



class RequirementSerializer(serializers.Serializer):
    model = Requirement
    character_class = CharacterClassSerializer()
    fields = '__all__'