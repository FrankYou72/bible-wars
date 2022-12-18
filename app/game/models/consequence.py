from django.db.models import Model, CharField, IntegerField
from rest_framework import serializers

from ...utils.exceptions import IncorrectInstance
from ...utils.operations import inverses



class Consequence(Model):
    description = CharField(max_length=255, null=True)
    instance = CharField(max_length=32, null=True)
    attribute = CharField(max_length=32, null=True)
    operation = CharField(max_length=4, null=True)
    factor = IntegerField(null=True)


    class Meta:
        db_table = '"game"."consequence"'
        managed = True

    def __str__(self):
        return f'{self.attribute}: {self.operation} {self.factor}'

    def apply(self, object, permanent=False):
        if object.__class__.__name__ != self.instance:
            raise IncorrectInstance

        command = f"object.{self.attribute} = object.{self.attribute} {self.operation} {self.factor}"
        exec(command)

        if permanent:
            object.save()

    def unnapply(self, object):
        if object.__class__.__name__ != self.instance:
            raise IncorrectInstance

        inverse_op = inverses[self.operation]

        command = f"object.{self.attribute} = object.{self.attribute} {inverse_op} {self.factor}"
        exec(command)


class ConsequenceSerializer(serializers.Serializer):
    model = Consequence
    fields = '__all__'