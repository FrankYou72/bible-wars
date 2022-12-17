from django.db.models import Model, CharField, IntegerField



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
