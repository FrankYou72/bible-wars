from django.db.models import Model, CharField, TextField, BooleanField, ForeignKey, PROTECT

from .consequence import Consequence
from .requirement import Requirement


class Event(Model):
    name = CharField(max_length=128, null=True)
    description = TextField(null=True)
    requirement = ForeignKey(Requirement, null=True, on_delete=PROTECT)
    consequence = ForeignKey(Consequence, null=True, on_delete=PROTECT)
    spiritual_intervention = BooleanField(null=True)
    is_global = BooleanField(null=True)

    class Meta:
        db_table = '"game"."event"'
        managed = True

    def __str__(self):
        return self.name
