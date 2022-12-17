from django.db.models import Model, CharField


class CardType(Model):
    name = CharField(max_length=128, null=True)
    identifier = CharField(max_length=16, primary_key=True)

    class Meta:
        #db_table = '"game"."card_type"'
        managed = True

    def __str__(self):
        return self.name
