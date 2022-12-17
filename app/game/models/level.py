from django.db.models import Model, CharField, IntegerField, ForeignKey, PROTECT

from .character import Character


class Level(Model):
    number = IntegerField(null=True)
    slate = CharField(max_length=64, null=True)
    character = ForeignKey(Character, null=True, on_delete=PROTECT)


    class Meta:
        db_table = '"game"."level"'
        managed = True

    def __str__(self):
        return self.slate
