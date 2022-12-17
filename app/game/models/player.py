from django.db.models import Model, CharField, TextField, ForeignKey, IntegerField, BooleanField, PROTECT
from django.contrib.auth.models import User

from .character import Character
from .match import Match


class Player(Model):
    character = ForeignKey(Character, null=True, on_delete=PROTECT)
    match = ForeignKey(Match, null=True, on_delete=PROTECT)
    level = IntegerField(null=True)
    score = IntegerField(null=True)
    lives = IntegerField(null=True)
    is_alive = BooleanField(null=True)
    user = ForeignKey(User, null=True, on_delete=PROTECT)


    class Meta:
        db_table = '"game"."player"'
        managed = True

    def __str__(self):
        return self.user
