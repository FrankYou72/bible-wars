from django.db.models import Model, IntegerField



class Body(Model):
    head = IntegerField(null=True)
    cover = IntegerField(null=True)
    left_arm = IntegerField(null=True)
    right_arm = IntegerField(null=True)
    feet = IntegerField(null=True)


    class Meta:
        #db_table = '"game"."body"'
        managed = True

    def __str__(self):
        return self.id
